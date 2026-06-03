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
            <div style="width: 100%;display: flex;flex-direction: column;;margin-top: 50px;">
                <div v-if="is_advanced" class="form_title" style="width: 100%;">
                    <v-text-field
                        v-model="title"
                        color="deep-purple"
                        label="Title"
                        variant="filled"
                        style="width: 100%;"
                    ></v-text-field>
                </div>
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
                        style=""
                    ></v-textarea>
                    <!-- <v-btn
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
                    </v-btn> -->
                </div>
                <div v-if="is_advanced" class="form_tag">
                    <v-text-field
                        v-model="tag"
                        color="deep-purple"
                        label="Tag"
                        variant="filled"
                        style="width: 100%;"
                    ></v-text-field>
                </div>
                <div v-if="is_advanced" class="form_language" style="width: 100%;">
                    <v-select
                        v-model="language"
                        :items="form_language_options"
                        item-title="label"
                        item-value="value"
                        color="deep-purple"
                        label="Language"
                        variant="filled"
                        style="width: 100%;"
                    ></v-select>
                </div>
                <div style="padding-right: 0px;display: flex;justify-content: flex-end;">
                    <a href="http://funding.wiki:8000/issue/add/?operation=KICKSTART&show_advance=1" style="color: blue; text-decoration: none;">Advanced</a>
                </div>
                <div style="display: flex; justify-content: center;width:100%">
                    <div class="form_btn" style="width: 320px;margin-top: 10px;display: flex;justify-content: space-between;">
                        <v-btn
                            class="text-none"
                            color="white"
                            variant="filled"
                            :loading="loading"
                            @click="submitForm"
                            border="none"
                            style="margin-right: 10px;background:#F58224;"
                        >
                            Public search
                        </v-btn>
                        <v-btn
                            class="text-none"
                            color="blue"
                            variant="outlined"
                            border="none"
                            style="background-color: #E1ECF4;"
                        >
                            Private project
                        </v-btn>
                    </div>
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
import { useRouter } from 'vue-router'
import {getCookie, setUserCookie} from '@/utils/cookies.js'
import {getIdeas, getIdeasInterested, saveIdea} from '../services/ideas.js'
import {isUserLogin} from '../services/user.js'
import {getLanguages} from '../services/language.js'

import { CdxIcon } from '@wikimedia/codex';
import { cdxIconBell } from '@wikimedia/codex-icons';

import User from './User.vue'
import IdeaItem from './IdeaItem.vue'
import MyIdeas from './MyIdeas.vue'

import {imageUrl} from '@/utils/util.js'

const router = useRouter()

const form_language_options = ref([
    {
        label: 'English',
        value: 'en'
    },
    {
        label: 'Spanish',
        value: 'es'
    },
    {
        label: 'French',
        value: 'fr'
    },
])

const is_advanced = ref(false)

const idea_content = ref('')

const title = ref('')
const tags = ref('')
const language = ref('en')

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
    const content = idea_content.value.trim()
    const wordCount = content.split(/\s+/).filter(Boolean).length
    if (wordCount === 1) {
        router.push({ path: '/issuelist', query: { show_my_new_issue: '0', search: content } })
        return
    }

    loading.value = true
    const { valid } = await form.value.validate()
    if (valid) {
        let response = await saveIdea(idea_content.value)
        console.log(response.data)
        form_success.value = true

        myIdeasKey.value += 1
        ideas_list.value = await getIdeasInterested()

        loading.value = false

        router.push({ path: '/issuelist', query: { show_my_new_issue: '1' } })
        // setTimeout(() => {
        //     form_success.value = false
        //     idea_content.value = ''
        // }, 2000)
    }else{
        loading.value = false
    }
}

const ideas_list = ref([])
var loadIdeas = async ()=>{
    ideas_list.value = await getIdeasInterested()
}

var loadLanguages = async ()=>{
    let languages = await getLanguages()
    console.log(languages)
    form_language_options.value = languages.map((language) => ({
        label: language.name,
        value: language.code
    }))
}

const is_user_login = ref(false)
onMounted(async ()=>{
    loadIdeas()
    is_user_login.value = await isUserLogin()
    setUserCookie()
    loadLanguages()
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