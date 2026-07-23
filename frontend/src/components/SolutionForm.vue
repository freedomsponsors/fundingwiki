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
                    label=""
                    rows="5"
                    auto-grow
                    autofocus
                    :rules="content_not_empty"
                    style=""
                ></v-textarea>
                <v-btn
                    class="text-none"
                    color="blue"
                    variant="outlined"
                    border="none"
                    :loading="loading"
                    @click="submitForm"
                    style="background-color: #E1ECF4;"
                >{{currentEditSolution ? 'Edit' : 'Submit'}} solution</v-btn>
                <a v-if="currentEditSolution || form_content" @click="form_content='';currentEditSolution=null" style="margin-left: 10px;">Cancel</a>
            </div>
        </div>
    </v-form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { saveSolution } from '@/services/solution.js'

const props = defineProps({
    issue: {
        type: Object,
        required: true
    },
    editingSolution: {
        type: Object,
        default: null
    }
})

const form_content = ref('')
const loading = ref(false)
const isValid = ref(false)
const form = ref(null)
const form_success = ref(false)
const currentEditSolution = ref(null)

const emit = defineEmits(['submit-success'])

const content_not_empty = [
    value => {
        if (value) return true
        return 'You must write something to submit.'
    },
]

watch(() => props.editingSolution, (solution) => {
    if (solution && solution.content) {
        currentEditSolution.value = solution
        form_content.value = solution.content
    } else {
        form_content.value = ''
    }
}, { immediate: true })

const submitForm = async () => {
    const content = form_content.value.trim()

    if (!content) {
        return
    }

    loading.value = true
    const { valid } = await form.value.validate()
    if (valid) {
        const solutionId = currentEditSolution?.value.id ?? null
        let response = await saveSolution(props.issue.id, form_content.value, solutionId)
        console.log(response)
        form_success.value = true

        loading.value = false

        form_success.value = false
        form_content.value = ''
        currentEditSolution.value = null

        emit('submit-success')
    } else {
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