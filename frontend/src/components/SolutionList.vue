<template>
    <div v-if="data_list.length > 0" style="width: 650px;">
        <div v-if="data_list.length == 1" class="page_section_title"><h2>1 Proposed solution</h2></div>
        <div v-else class="page_section_title"><h2>{{ data_list.length }} Proposed solutions</h2></div>
        <div>
            <div class="solution-item" v-for="(item, index) in data_list" :key="index">
                {{ item.content }}
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import {getSolution} from '@/services/solution.js'

const data_list = ref([])

const props = defineProps({
    issue: {
        type: Object,
        required: true
    }
})
console.log(props.issue.id)

// onMounted(async ()=>{
//     data_list.value = await getSolution(props.issue.id)
// })

watch(() => props.issue.id, (newVal, oldVal) => {
    if (newVal) {
        getSolution(newVal).then((response) => {
            data_list.value = response
        })
    }
}, { deep: true })

</script>

<style scoped>
.solution-item {
    width: 100%;
    border-bottom: 1px solid #efefef;
    padding: 10px 0;
}
.page_section_title{
    border-bottom: 1px solid #efefef;
    margin-bottom: 10px;
    margin-top: 20px;
}
</style>
