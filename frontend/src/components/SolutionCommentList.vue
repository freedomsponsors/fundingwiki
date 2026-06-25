<template>
    <div v-if="data_list.length > 0" style="width: 100%;background-color: #f9f9f9;padding: 10px;">
        <div v-if="data_list.length == 1" class="page_section_title">1 Comment</div>
        <div v-else class="page_section_title">{{ data_list.length }} Comments</div>
        <div style="">
            <div class="solution-item" v-for="(item, index) in data_list" :key="index">
                <div>
                    <div>
                        <span style="color: #007bff;">{{ item.author.username }}</span>
                        <span style="color: #ccc;padding-left:10px;font-size:14px">{{ relativeTimeFrom(item.creationDate) }}</span>
                    </div>
                    <div>{{ item.content }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { relativeTimeFrom } from '@/utils/util.js'

const data_list = ref([])

const props = defineProps({
    comment_list: {
        type: Array,
        required: true
    }
})

onMounted(async () => {
    data_list.value = props.comment_list
})

watch(
    () => props.comment_list,
    async (newVal) => {
        if (newVal) {
            data_list.value = newVal
        }
    },
    { deep: true }
)
</script>

<style scoped>
.solution-item {
    width: 100%;
    border-bottom: 1px solid #f3f1f1;
    padding: 10px 0;
}
.page_section_title{
    border-bottom: 1px solid #efefef;
    font-size: 18px;
}
.solution-meta{
    text-align: right;
    color: #888;
}
</style>
