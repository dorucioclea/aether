/**
 * https://github.com/yahoo/react-intl/wiki/Testing-with-React-Intl#enzyme
 *
 * Components using the react-intl module require access to the intl context.
 * This is not available when mounting single components in Enzyme.
 * These helper functions aim to address that and wrap a valid,
 * English-locale intl context around them.
 */

import React from 'react'
import { IntlProvider, intlShape } from 'react-intl'
import { mount, shallow, render } from 'enzyme'

// You can pass your messages to the IntlProvider. Optional: remove if unneeded.
const messages = require('./locales/en')

// Create the IntlProvider to retrieve context for wrapping around.
const intlProvider = new IntlProvider({ locale: 'en', messages }, {})
const { intl } = intlProvider.getChildContext()

/**
 * When using React-Intl `injectIntl` on components, props.intl is required.
 */
const nodeWithIntlProp = (node) => React.cloneElement(<IntlProvider>{node}</IntlProvider>, { intl })

export const shallowWithIntl = (node, { context, ...additionalOptions } = {}) => shallow(
  nodeWithIntlProp(node),
  {
    context: Object.assign({}, context, { intl }),
    ...additionalOptions
  }
)

export const mountWithIntl = (node, { context, childContextTypes, ...additionalOptions } = {}) => mount(
  nodeWithIntlProp(node),
  {
    context: Object.assign({}, context, { intl }),
    childContextTypes: Object.assign({}, { intl: intlShape }, childContextTypes),
    ...additionalOptions
  }
)

export const renderWithIntl = (node, { context, childContextTypes, ...additionalOptions } = {}) => render(
  nodeWithIntlProp(node),
  {
    context: Object.assign({}, context, { intl }),
    childContextTypes: Object.assign({}, { intl: intlShape }, childContextTypes),
    ...additionalOptions
  }
)
