<template>
    <v-form 
        ref="form" 
        v-model="isValid" 
        lazy-validation 
        validate-on="submit"
        style="width: 100%;">
        <div style="width: 100%;">
            <div style="">
                <v-textarea
                    v-model="form_content"
                    label="Add a comment"
                    rows="1"
                    auto-grow
                    :rules="content_not_empty"
                    @focus="isFocus = true"
                    @blur="isFocus = false"
                    style=""
                ></v-textarea>
                <v-btn
                    v-show="isFocus || form_content.trim() !== ''"
                    class="text-none"
                    color="blue"
                    variant="outlined"
                    border="none"
                    :loading="loading"
                    @click="submitForm"
                    style="background-color: #E1ECF4;"
                >Comment</v-btn>
            </div>
        </div>
    </v-form>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, emit } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import {getCookie, setUserCookie} from '@/utils/cookies.js'
import {saveSolutionComment} from '@/services/solution_comment.js'
import {isUserLogin} from '@/services/user.js'

const props = defineProps({
    solution: {
        type: Object,
        required: true
    }
})
console.log(props.solution.id)

const isFocus = ref(false)

const router = useRouter()

const show_my_new_issue = ref(false)

const form_content = ref('')

const loading = ref(false)
const isValid = ref(false)
const form = ref(null)
const form_success = ref(false)
const myIdeasKey = ref(0)

const emit = defineEmits(['submit-success'])

const content_not_empty = [
    value => {
        if (value) return true
        return 'You must write something to submit.'
    },
]

const submitForm = async () => {
    const content = form_content.value.trim()

    loading.value = true
    const { valid } = await form.value.validate()
    if (valid) {
        let response = await saveSolutionComment(props.solution.id, form_content.value)
        console.log(response.data)
        form_success.value = true

        loading.value = false

        form_success.value = false
        form_content.value = ''

        // Emit an event to notify the parent component to refresh the solution list
        emit('submit-success')
    }else{
        loading.value = false
    }
}
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