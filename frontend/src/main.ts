import { createApp } from 'vue'
import './style.css'

// Vuetify setup
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'

const vuetify = createVuetify({ components, directives })

const app = createApp(App)

// register global component
import ConfirmDialog from './components/common/ConfirmDialog.vue'
app.component('ConfirmDialog', ConfirmDialog)

app.use(vuetify).mount('#app')
