<template>
<div>
    <User></User>
</div>
<div style="display: flex;align-items: center;margin-top: 50px;margin-bottom: 100px;flex-direction: column;">
    <div style="display: flex;flex-direction: column; align-items: center;width: 650px;gap: 20px;">
        <div style="display:flex;align-items:center;">
            <img :src="imageUrl('/static/img/fundingwiki-logo-fit_80x107px-v1.0.png')" style="width: 70px;"/>
            <h1 style="padding-left:10px">Brainstorm or find inspiration!</h1>
        </div>
        <v-form 
            v-if="!form_success"
            ref="form" 
            v-model="isValid" 
            lazy-validation 
            validate-on="submit"
            style="width: 100%;">
            <div style="width: 100%;display: flex;flex-direction: column;align-items: center;margin-top: 50px;">
                <div style="width: 100%;position: relative;">
                    <v-textarea
                        v-model="idea_content"
                        color="deep-purple"
                        label="What's on your mind?"
                        rows="3"
                        variant="filled"
                        auto-grow
                        autofocus
                        :rules="content_not_empty"
                        style="padding-right: 50px;"
                    ></v-textarea>
                    <v-btn
                        style="position: absolute; right: 8px; bottom: 8px;"
                        :disabled="loading"
                        :loading="loading"
                        color="grey-lighten-2"
                        size="36"
                        variant="text"
                        @click="submitForm"
                        icon
                        class="no-box-shadow"
                    >
                        <v-icon size="24" color="grey-darken-1">las la-arrow-circle-up</v-icon>
                    </v-btn>
                </div>
            </div>
        </v-form>

        <div v-if="form_success" style="width: 100%;">
            <v-textarea
                v-model="idea_content"
                color="deep-purple"
                label="What's on your mind?"
                rows="3"
                variant="filled"
                auto-grow
                readonly
                style="background-color: rgba(76, 175, 80, 0.3); transition: background-color 2s;"
            ></v-textarea>
        </div>


        
        <div style="width: 100%;">
            <div style="width: 100%;">
                <MyIdeas :key="myIdeasKey"></MyIdeas>
            </div>
            <div v-if="ideas_list.length > 0" style="width: 100%;">
                <div style="width: 100%;margin-top: 60px;border-bottom: 1px solid #efefef;"><h3>Related ideas</h3></div>
                <div style="width: 100%;">
                    <div v-for="(idea, index) in ideas_list" :key="index" class="idea_item">
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
import {getCookie, setUserCookie} from '@/utils/cookies.js'
import {getIdeas, getIdeasInterested, saveIdea} from '@/services/ideas.js'
import {isUserLogin} from '@/services/user.js'

import User from './User.vue'
import IdeaItem from './IdeaItem.vue'
import MyIdeas from './MyIdeas.vue'

import {imageUrl} from '@/utils/util.js'

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
    loading.value = true
    const { valid } = await form.value.validate()
    if (valid) {
        let response = await saveIdea(idea_content.value)
        console.log(response.data)
        form_success.value = true

        myIdeasKey.value += 1
        ideas_list.value = await getIdeasInterested()

        loading.value = false

        setTimeout(() => {
            form_success.value = false
            idea_content.value = ''
        }, 2000)
    }else{
        loading.value = false
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