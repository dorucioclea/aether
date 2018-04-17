// Combines types, actions and reducers for a specific
// module in one file for easy redux management

import { clone } from '../utils'
import urls from '../utils/urls'

export const types = {
  PIPELINE_UPDATE: 'pipeline_update',
  PIPELINE_ADD: 'pipeline_add',
  PIPELINE_LIST_CHANGED: 'pipeline_list_changed',
  SELECTED_PIPELINE_CHANGED: 'selected_pipeline_changed',
  TEST_API_CALL: 'test_api_call',
  TEST_API_FAILED: 'test_api_failed'
}

const INITIAL_PIPELINE = {
  pipelineList: [],
  selectedPipeline: null,
  test: null
}

export const addPipeline = newPipeline => ({
  // TODO: Change 3rd param to action on request failure when ui endpoints are available
  // types: ['', types.PIPELINE_ADD, types.PIPELINE_ADD],
  // promise: client => client.post(urls.PIPELINE_URL, 'application/x-www-form-urlencoded', {
  //   data: newPipeline
  // })
  type: types.PIPELINE_ADD,
  payload: newPipeline
})

export const selectedPipelineChanged = selectedPipeline => ({
  type: types.SELECTED_PIPELINE_CHANGED,
  payload: selectedPipeline
})

export const getAPICALL = () => ({
  types: ['', types.TEST_API_CALL, types.TEST_API_FAILED],
  promise: client => client.get(urls.SAMPLE_URL, 'application/json')
})

const reducer = (state = INITIAL_PIPELINE, action = {}) => {
  const newPipelineList = clone(state.pipelineList)
  const findIndex = arr => arr.findIndex(x => x.id === action.payload.id)

  switch (action.type) {
    case types.PIPELINE_ADD: {
      newPipelineList.unshift(action.payload)
      return { ...state, pipelineList: newPipelineList }
    }

    case types.PIPELINE_UPDATE: {
      const index = findIndex(newPipelineList)
      newPipelineList[index] = action.payload
      return { ...state, pipelineList: newPipelineList }
    }

    case types.SELECTED_PIPELINE_CHANGED: {
      return { ...state, selectedPipeline: action.payload }
    }

    case types.TEST_API_CALL: {
      return { ...state, test: action.payload }
    }

    case types.TEST_API_FAILED: {
      return { ...state, test: action.error }
    }

    default:
      return state
  }
}

export default reducer
