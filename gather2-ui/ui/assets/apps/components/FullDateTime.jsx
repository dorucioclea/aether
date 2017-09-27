import React, { Component } from 'react'
import {
  FormattedDate,
  FormattedRelative,
  FormattedTime
} from 'react-intl'

export default class FullDateTime extends Component {
  render () {
    const {date} = this.props
    if (!date) {
      return <div />
    }

    return (
      <span>
        <span className='mr-2'>
          <FormattedDate
            value={date}
            year='numeric'
            month='long'
            day='numeric' />
        </span>
        <span className='mr-2'>
          <FormattedTime
            value={date}
            hour12={false}
            hour='2-digit'
            minute='2-digit'
            second='2-digit'
            timeZoneName='short' />
        </span>
        <span>
          (<FormattedRelative value={date} />)
        </span>
      </span>
    )
  }
}
