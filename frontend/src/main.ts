import { createApp } from 'vue'
import './style.css'
// import App from './App.vue'

// Vuetify setup
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({ components, directives })

// const app = createApp(App)
// app.use(vuetify).mount('#app')  .rst

document.querySelectorAll('[data-component]').forEach(el => {
    const componentName = el.dataset.component
    console.log(componentName)
    // import(`./components/${componentName}.vue`).then(PageComponent => {
    
    import('./components/'+componentName+'.vue').then(PageComponent => {
        console.log(componentName)
        console.log(PageComponent)

        // app.component(componentName, PageComponent.default)
        // app.use(vuetify).mount(el)
        createApp(PageComponent.default).use(vuetify).mount(el)
    })
})