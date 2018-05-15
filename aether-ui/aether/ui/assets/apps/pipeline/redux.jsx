// Combines types, actions and reducers for a specific
// module in one file for easy redux management

import { clone } from '../utils'
import urls from '../utils/urls'

export const types = {
  PIPELINE_ADD: 'pipeline_add',
  PIPELINE_UPDATE: 'pipeline_update',

  PIPELINE_LIST_CHANGED: 'pipeline_list_changed',
  SELECTED_PIPELINE_CHANGED: 'selected_pipeline_changed',
  GET_ALL: 'pipeline_get_all',
  PIPELINE_ERROR: 'pipeline_error',
  GET_BY_ID: 'pipeline_get_by_id',
  PIPELINE_NOT_FOUND: 'pipeline_not_found'
}

export const INITIAL_PIPELINE = {
  pipelineList: [],
  selectedPipeline: null,
  error: null,
  notFound: null
}

export const addPipeline = ({ name }) => ({
  types: ['', types.PIPELINE_ADD, types.PIPELINE_ERROR],
  promise: client => client.post(
    `${urls.PIPELINES_URL}`,
    { 'Content-Type': 'application/json' },
    { data: { name } })
})

export const getPipelineById = id => ({
  types: ['', types.PIPELINE_UPDATE, types.PIPELINE_NOT_FOUND],
  promise: client => client.get(
    `${urls.PIPELINES_URL}${id}/`,
    { 'Content-Type': 'application/json' }
  )
})

export const updatePipeline = pipeline => ({
  types: ['', types.PIPELINE_UPDATE, types.PIPELINE_ERROR],
  promise: client => client.put(
    `${urls.PIPELINES_URL}${pipeline.id}/`,
    { 'Content-Type': 'application/json' },
    { data: pipeline }
  )
})

export const selectedPipelineChanged = selectedPipeline => ({
  type: types.SELECTED_PIPELINE_CHANGED,
  payload: selectedPipeline
})

export const getPipelines = () => ({
  types: ['', types.GET_ALL, types.PIPELINE_ERROR],
  promise: client => client.get(
    // limit query_string used instead of pagination (temporary)
    `${urls.PIPELINES_URL}?limit=5000`,
    { 'Content-Type': 'application/json' }
  )
})

const parsePipeline = (pipeline) => {
  const COLORS = 10 // This value is the number of colors in the `_color-codes.scss`
  // will highlight the relations among mapping rules, entity types and input schema
  const highlightSource = {}
  const highlightDestination = []

  // each EntityType has a color based on the order it was added to the list
  const entityColors = {}
  const entityTypes = (pipeline.entity_types || [])
  entityTypes.forEach((entity, index) => {
    entityColors[entity.name] = (index % COLORS) + 1
  })

  // indicate the color to each JSON path in each rule source and destination
  const mappingRules = (pipeline.mapping || [])
  mappingRules.forEach(rule => {
    // find out the number assigned to the linked Entity Type
    const entityType = rule.destination.split('.')[0]
    const color = entityColors[entityType] || 0

    highlightSource[rule.source] = color
    highlightDestination.push(rule.destination)
  })

  return {
    ...clone(pipeline),
    highlightSource,
    highlightDestination
  }
}

const reducer = (state = INITIAL_PIPELINE, action) => {
  const newPipelineList = clone(state.pipelineList)

  switch (action.type) {
    case types.PIPELINE_ADD: {
      const newPipeline = parsePipeline(action.payload)
      newPipelineList.unshift(newPipeline)
      return { ...state, pipelineList: newPipelineList, selectedPipeline: newPipeline, error: null }
    }

    case types.PIPELINE_UPDATE: {
      const updatedPipeline = parsePipeline({ ...state.selectedPipeline, ...action.payload })
      const index = newPipelineList.findIndex(x => x.id === updatedPipeline.id)
      newPipelineList[index] = updatedPipeline

      return { ...state, pipelineList: newPipelineList, selectedPipeline: updatedPipeline, error: null }
    }

    case types.SELECTED_PIPELINE_CHANGED: {
      return { ...state, selectedPipeline: parsePipeline(action.payload), error: null }
    }

    case types.GET_ALL: {
      return { ...state, pipelineList: action.payload.results || [], error: null }
    }

    case types.PIPELINE_ERROR: {
      return { ...state, error: action.error }
    }

    case types.PIPELINE_NOT_FOUND: {
      return { ...state, notFound: action.error, selectedPipeline: null }
    }

    default:
      return state
  }
}

export default reducer
