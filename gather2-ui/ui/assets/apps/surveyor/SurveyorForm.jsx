import React, { Component } from 'react'
import { defineMessages, injectIntl, FormattedMessage } from 'react-intl'

import { clone } from '../utils'
import { deleteData, postData, putData } from '../utils/request'

import { ConfirmButton, ErrorAlert, WarningAlert } from '../components'

const MESSAGES = defineMessages({
  addTitle: {
    defaultMessage: 'New surveyor',
    id: 'surveyor.form.title.add'
  },
  editTitle: {
    defaultMessage: 'Edit surveyor',
    id: 'surveyor.form.title.edit'
  },

  deleteButton: {
    defaultMessage: 'Delete surveyor',
    id: 'surveyor.form.action.delete'
  },
  deleteConfirm: {
    defaultMessage: 'Are you sure you want to delete the surveyor “{username}”?',
    id: 'surveyor.form.action.delete.confirm'
  },
  deleteError: {
    defaultMessage: 'An error occurred while deleting “{username}”',
    id: 'surveyor.form.action.delete.error'
  },
  submitError: {
    defaultMessage: 'An error occurred while saving “{username}”',
    id: 'surveyor.form.action.submit.error'
  },

  passwordLengthWarning: {
    defaultMessage: 'The password must contain at least 10 characters.',
    id: 'surveyor.form.password.warning.length'
  },
  passwordSimilarWarning: {
    defaultMessage: 'The password can\'t be too similar to your other personal information.',
    id: 'surveyor.form.password.warning.similar'
  },
  passwordCommonWarning: {
    defaultMessage: 'The password can\'t be a commonly used password.',
    id: 'surveyor.form.password.warning.common'
  },
  passwordNumericWarning: {
    defaultMessage: 'The password can\'t be entirely numeric.',
    id: 'surveyor.form.password.warning.numeric'
  },

  passwordRepeatedError: {
    defaultMessage: 'The two password fields didn\'t match.',
    id: 'surveyor.form.password.error.repeated'
  },
  passwordShortError: {
    defaultMessage: 'This password is too short. It must contain at least 10 characters.',
    id: 'surveyor.form.password.error.length'
  }
})

export class SurveyorForm extends Component {
  constructor (props) {
    super(props)
    this.state = { ...clone(this.props.surveyor), errors: {} }
  }

  render () {
    const {formatMessage} = this.props.intl
    const surveyor = this.state
    const isNew = (surveyor.id === undefined)

    const title = (
      isNew
      ? <FormattedMessage
            id='surveyor.form.title.add'
            defaultMessage='New surveyor' />
      : (
        <span>
          <FormattedMessage
            id='surveyor.form.title.edit'
            defaultMessage='Edit surveyor' />
          <span className='username ml-2'><i className='fa fa-user mr-1' />{this.props.surveyor.username}</span>
        </span>
        )
    )
    const dataQA = (
      isNew
      ? 'surveyor-add'
      : `surveyor-edit-${surveyor.id}`
    )

    return (
      <div data-qa={dataQA} className='surveyor-edit'>
        <h3 className='page-title'>{title}</h3>

        <ErrorAlert errors={surveyor.errors.global} />

        <form onSubmit={this.onSubmit.bind(this)}>
          <div className='form-group big-input'>
            <label className='form-control-label title'>
              <FormattedMessage
                id='surveyor.form.username'
                defaultMessage='Surveyor username' />
            </label>
            <input
              name='username'
              type='text'
              className='form-control'
              required
              value={surveyor.username || ''}
              onChange={this.onInputChange.bind(this)}
            />
            <ErrorAlert errors={surveyor.errors.username} />
          </div>

          <div className='form-group big-input'>
            <label className='form-control-label title'>
              <FormattedMessage
                id='surveyor.form.password'
                defaultMessage='Password' />
            </label>
            <input
              name='password_1'
              type='password'
              className='form-control'
              required={isNew}
              value={surveyor.password_1 || ''}
              onChange={this.onInputChange.bind(this)}
            />
            <ErrorAlert errors={surveyor.errors.password} />

            <WarningAlert
              warnings={[
                formatMessage(MESSAGES.passwordLengthWarning),
                formatMessage(MESSAGES.passwordSimilarWarning),
                formatMessage(MESSAGES.passwordCommonWarning),
                formatMessage(MESSAGES.passwordNumericWarning)
              ]}
            />
          </div>

          <div className='form-group big-input'>
            <label className='form-control-label title'>
              <FormattedMessage
                id='surveyor.form.password.repeat'
                defaultMessage='Repeat password' />
            </label>
            <input
              name='password_2'
              type='password'
              className='form-control'
              required={isNew || surveyor.password_1}
              value={surveyor.password_2 || ''}
              onChange={this.onInputChange.bind(this)}
            />
          </div>

          <div className='actions'>
            <div>
              { !isNew &&
                <ConfirmButton
                  className='btn btn-delete'
                  cancelable
                  onConfirm={this.onDelete.bind(this)}
                  title={title}
                  message={formatMessage(MESSAGES.deleteConfirm, {...this.props.surveyor})}
                  buttonLabel={formatMessage(MESSAGES.deleteButton)}
                />
              }
            </div>
            <div>
              <button
                type='button'
                className='btn btn-cancel btn-block'
                onClick={(evt) => this.props.onCancel(evt)}>
                <FormattedMessage
                  id='surveyor.form.action.cancel'
                  defaultMessage='Cancel' />
              </button>
            </div>
            <div>
              <button type='submit' className='btn btn-primary btn-block'>
                <FormattedMessage
                  id='surveyor.form.action.submit'
                  defaultMessage='Save surveyor' />
              </button>
            </div>
          </div>
        </form>
      </div>
    )
  }

  onInputChange (event) {
    event.preventDefault()
    this.setState({ [event.target.name]: event.target.value })
  }

  validatePassword () {
    const {formatMessage} = this.props.intl

    if (!this.state.id || this.state.password_1) {
      // validate password
      if (this.state.password_1 !== this.state.password_2) {
        this.setState({
          errors: {
            password: [formatMessage(MESSAGES.passwordRepeatedError)]
          }
        })
        return false
      }

      if (this.state.password_1.length < 10) {
        this.setState({
          errors: {
            password: [formatMessage(MESSAGES.passwordShortError)]
          }
        })
        return false
      }
    }

    return true
  }

  onSubmit (event) {
    event.preventDefault()
    this.setState({ errors: {} })

    if (!this.validatePassword()) {
      return
    }

    const {formatMessage} = this.props.intl
    const surveyor = {
      username: this.state.username,
      password: this.state.password_1 || this.props.surveyor.password
    }

    const saveMethod = (this.state.id ? putData : postData)
    const url = '/odk/surveyors' + (this.state.id ? '/' + this.state.id : '') + '.json'

    return saveMethod(url, surveyor)
      .then(response => {
        // navigate to Surveyors list page
        window.location.pathname = '/surveyors'
      })
      .catch(error => {
        console.log(error.message)
        error.response
          .then(resp => {
            this.setState({ errors: resp })
          })
          .catch(() => {
            this.setState({
              errors: {
                global: [formatMessage(MESSAGES.submitError, {...surveyor})]
              }
            })
          })
      })
  }

  onDelete () {
    const {formatMessage} = this.props.intl
    const surveyor = this.state

    return deleteData(`/odk/surveyors/${surveyor.id}.json`)
      .then(() => {
        // navigate to Surveyors list page
        window.location.pathname = '/surveyors'
      })
      .catch(error => {
        console.log(error.message)
        this.setState({
          errors: {
            global: [formatMessage(MESSAGES.deleteError, {...surveyor})]
          }
        })
      })
  }
}

// Include this to enable `this.props.intl` for this component.
export default injectIntl(SurveyorForm)
