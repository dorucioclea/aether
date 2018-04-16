import React, { Component } from 'react'
import { FormattedMessage } from 'react-intl'
import { generateGUID } from '../utils'

const PropertyList = props => {
  const result = []
  if (props.fields && props.fields.length) {
    props.fields.forEach(field => {
      if (field.type.fields) {
        let parent = null
        if (props.parent) {
          parent = `${props.parent}.${field.name}`
        } else {
          parent = field.name
        }
        result.push(PropertyList({fields: field.type.fields, parent: parent}))
      } else {
        let fieldType = ''
        if (typeof field.type === 'object') {
          fieldType = `[${field.type.symbols ? field.type.symbols.toString() : field.type.name}]`
        } else {
          fieldType = field.type
        }
        if (props.parent) {
          result.push(<div key={`${props.parent}.${field.name}`}><span>{`${props.parent}.${field.name}`}</span>&nbsp;&nbsp;
            <span>{fieldType}</span></div>)
        } else {
          result.push(<div key={field.name}><span>{field.name}</span>&nbsp;&nbsp;
            <span>{fieldType}</span>
          </div>)
        }
      }
    })
    return result
  } else {
    return (<FormattedMessage
      id='entityTypes.entity.empty.properties.message'
      defaultMessage='Entity has no properties'
    />)
  }
}

const EntityTypeView = props => {
  return (<div>
    <h2>{props.name}</h2>
    <PropertyList fields={props.fields} />
  </div>)
}

class EntityTypeViewer extends Component {
  iterateTypes (entityTypesText) {
    try {
      const entityTypes = JSON.parse(entityTypesText)
      const result = []
      if (entityTypes && entityTypes.length) {
        entityTypes.forEach(entityType => {
          if (entityType.name && entityType.fields) {
            result.push(<EntityTypeView name={entityType.name} fields={entityType.fields} key={entityType.name} />)
          } else {
            result.push(<div className='hint' key={generateGUID()}>
              <FormattedMessage
                id='entityTypes.entity.invalid.message'
                defaultMessage='Invalid entity type'
              />
            </div>)
          }
        })
        return result
      } else {
        return (<div className='hint'>
          <FormattedMessage
            id='entityTypes.entity.invalid.schema'
            defaultMessage='Invalid schema'
          />
        </div>)
      }
    } catch (error) {
      return (<div className='hint'>
        <FormattedMessage
          id='entityTypes.entity.invalid.schema'
          defaultMessage='Invalid JSON'
        />
      </div>)
    }
  }

  render () {
    if (!this.props.schema) {
      return (<div className='hint'>
        <FormattedMessage
          id='entityTypes.entity.empty.message'
          defaultMessage='No Entity Types added to your pipeline yet.'
        />
      </div>)
    }
    return (
      <div className='entity-types-schema'>
        { this.iterateTypes(this.props.schema) }
      </div>
    )
  }
}

export default EntityTypeViewer
