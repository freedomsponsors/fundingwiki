<template>
<div>
    <User></User>
</div>
<div style="display: flex;align-items: center;margin-top: 50px;margin-bottom: 100px;flex-direction: column;">
    <div style="display: flex;flex-direction: column; align-items: center;width: 650px;gap: 20px;">
        <div style="display:flex;align-items:center;">
            <img src="https://alfinal.eu.pythonanywhere.com/static/img/fundingwiki-logo-fit_80x107px-v1.0.png" style="width: 70px;"/>
            <h1 style="padding-left:10px">I have an idea!</h1>
        </div>
        <v-form 
            v-if="!form_success"
            ref="form" 
            v-model="isValid" 
            lazy-validation 
            validate-on="submit"
            style="width: 100%;">
            <div style="width: 100%;display: flex;flex-direction: column;align-items: center;margin-top: 50px;">
                <div style="width: 100%;">
                <v-textarea
                    v-model="idea_content"
                    color="deep-purple"
                    label="Write your idea here"
                    rows="3"
                    variant="filled"
                    auto-grow
                    autofocus
                    :rules="content_not_empty"
                ></v-textarea>
                </div>
                <div style="width: 200px;">
                    <v-btn
                        style="width: 100%;"
                        :disabled="loading"
                        :loading="loading"
                        class="text-none mb-4"
                        color="indigo-darken-3"
                        size="x-large"
                        variant="flat"
                        @click="submitForm"
                    >
                        Submit
                    </v-btn>
                </div>
            </div>
        </v-form>

        <v-alert
            v-if="form_success"
            title="Idea successfully submitted!"
            >
        </v-alert>
        <div style="width: 100%;">
            <div style="width: 100%;">
                <MyIdeas :key="myIdeasKey"></MyIdeas>
            </div>
            <div v-if="ideas_list.length > 0" style="width: 100%;">
                <div style="width: 100%;margin-top: 60px;border-bottom: 1px solid #efefef;"><h3>Ideas you may interested</h3></div>
                <div style="width: 100%;">
                    <div v-for="(idea, index) in ideas_list" :key="index" class="idea_item">
                        <!-- <div>{{ idea.content }}</div> -->
                        <IdeaItem :item="idea" @delete-idea="loadIdeas"></IdeaItem>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import axios from 'axios'
import {getCookie, setUserCookie} from '../utils/cookies.js'
import {getIdeas, getIdeasInterested, saveIdea} from '../services/ideas.js'
import {isUserLogin} from '../services/user.js'

import User from './User.vue'
import IdeaItem from './IdeaItem.vue'
import MyIdeas from './MyIdeas.vue'

const idea_content = ref('')
const loading = ref(false)
const isValid = ref(false)
const form = ref(null)
const form_success = ref(false)
const myIdeasKey = ref(0)

idea_content.value = ''

const content_not_empty = [
    value => {
        if (value) return true
        return 'You must write something to submit.'
    },
]

const submitForm = async () => {
    const { valid } = await form.value.validate()
    if (valid) {
        //var response = await axios.post('http://127.0.0.1:8000/vueapi/ideas', {
        //    idea_content: idea_content.value
        //},{
        //    headers: {
        //        'X-CSRFToken': getCookie('csrftoken'),
        //        'Content-Type': 'application/json'
        //   }
        //})

        let response = await saveIdea(idea_content.value)

        console.log(response.data)
        form_success.value = true
        
        myIdeasKey.value += 1
        ideas_list.value = await getIdeasInterested()

        setTimeout(() => {
            form_success.value = false
            idea_content.value = ''
        }, 3000)
    }
}

const ideas_list = ref([])
var loadIdeas = async ()=>{
    ideas_list.value = await getIdeasInterested()
}

const is_user_login = ref(false)
onMounted(async ()=>{
    loadIdeas()
    is_user_login.value = await isUserLogin()
    setUserCookie()
})
</script>

<style scoped>
.read-the-docs {
    color: #888;
}
.issue_title{
    text-align: left;
}
.idea_item{
    width: 100%;margin-top: 20px;border-bottom: 1px solid #efefef;
}
</style>
