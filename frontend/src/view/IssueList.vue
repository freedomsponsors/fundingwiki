<template>
<div>
    <User></User>
</div>
<div style="display: flex;align-items: center;margin-top: 50px;margin-bottom: 100px;flex-direction: column;">
    <div style="display: flex;flex-direction: column; align-items: center;width: 650px;gap: 20px;">
        <v-form 
            ref="form" 
            v-model="isValid" 
            lazy-validation 
            validate-on="submit"
            style="width: 100%;">
            <div style="width: 100%;display: flex;;margin-top: 50px;">
                <div style="flex-grow: 1;padding-right: 10px;">
                    <v-textarea
                        v-model="idea_content"
                        color="deep-purple"
                        label="What's on your mind?"
                        rows="5"
                        variant="filled"
                        auto-grow
                        autofocus
                        :rules="content_not_empty"
                        style=""
                    ></v-textarea>
                </div>
                <div style="width: 140px;">
                    <div class="form_btn" style="width: 320px;margin-top: 10px;display: flex; flex-direction: column;justify-content: space-between;gap:6px">
                        <v-btn
                            class="text-none"
                            color="white"
                            variant="filled"
                            :loading="loading"
                            @click="submitForm"
                            border="none"
                            style="margin-right: 10px;background:#F58224;width:130px"
                        >
                            Public search
                        </v-btn>
                        <a>Advanced search</a>
                        <v-btn
                            class="text-none"
                            color="blue"
                            variant="outlined"
                            border="none"
                            style="background-color: #E1ECF4;width:130px"
                        >
                            Private project
                        </v-btn>
                        <a href="http://funding.wiki:8000/issue/add/?operation=KICKSTART&show_advance=1">Advanced edition</a>
                    </div>
                </div>
            </div>
        </v-form>

        <div style="width: 100%;">
            <div v-if="show_my_new_issue" style="width: 100%;">
                <MyNewIssue :key="myIdeasKey"></MyNewIssue>
            </div>
            <div v-if="ideas_list.length > 0" style="width: 100%;">
                <div style="width: 100%;margin-top: 60px;border-bottom: 1px solid #efefef;"><h3>Interesting issues for you</h3></div>
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
import { useRoute } from 'vue-router'
import {getCookie, setUserCookie} from '@/utils/cookies.js'
import {getIdeas, getIdeasInterested, saveIdea} from '../services/ideas.js'
import {isUserLogin} from '../services/user.js'
import {getLanguages} from '../services/language.js'

import { CdxIcon } from '@wikimedia/codex';
import { cdxIconBell } from '@wikimedia/codex-icons';

import User from '../components/User.vue'
import IdeaItem from '../components/IdeaItem.vue'
import MyIdeas from '../components/MyIdeas.vue'
import MyNewIssue from '../components/MyNewIssue.vue'

import {imageUrl} from '@/utils/util.js'

const router = useRouter()

const show_my_new_issue = ref(false)

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
        // ideas_list.value = await getIdeasInterested()
        ideas_list.value = await getIdeas()

        loading.value = false

        router.push({ path: '/issuelist', query: { show_my_new_issue: '1' } })
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
    // ideas_list.value = await getIdeasInterested()
    ideas_list.value = await getIdeas()
}

const is_user_login = ref(false)
onMounted(async ()=>{
    const route = useRoute()
    if (route.query.show_my_new_issue === '1') {
        show_my_new_issue.value = true
    }
    if (route.query.search) {
        idea_content.value = route.query.search
    }
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