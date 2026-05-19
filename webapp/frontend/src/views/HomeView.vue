<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listAssessments, createAssessment, deleteAssessment } from '../api/client.js'

const router = useRouter()
const assessments = ref([])
const loading = ref(false)
const creating = ref(false)
const error = ref(null)

const form = ref({
  dataset_id: '',
  dataset_title: '',
  assessed_by: '',
  notes: '',
})

onMounted(fetchAssessments)

async function fetchAssessments() {
  loading.value = true
  try {
    const res = await listAssessments()
    assessments.value = res.data
  } catch (e) {
    error.value = 'Could not connect to API. Is the backend running?'
  } finally {
    loading.value = false
  }
}

async function startAssessment() {
  if (!form.value.dataset_id || !form.value.dataset_title) return
  creating.value = true
  try {
    const res = await createAssessment(form.value)
    router.push({ name: 'assess', params: { id: res.data.id } })
  } finally {
    creating.value = false
  }
}

async function removeAssessment(id) {
  await deleteAssessment(id)
  assessments.value = assessments.value.filter(a => a.id !== id)
}

const scoreColor = (score) => {
  if (score >= 70) return 'text-emerald-600'
  if (score >= 40) return 'text-amber-600'
  return 'text-red-500'
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <!-- Hero -->
    <div class="text-center mb-10">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        How FAIR is your data?
      </h1>
      <p class="text-gray-500 max-w-xl mx-auto">
        Answer questions across the 41 RDA FAIR Maturity Indicators and get an instant
        scorecard, gap analysis, and remediation roadmap.
      </p>
    </div>

    <!-- New assessment form -->
    <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 mb-10">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Start a New Assessment</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Dataset ID <span class="text-red-500">*</span></label>
          <input v-model="form.dataset_id" type="text" placeholder="e.g. STD-2024-CART-001"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Dataset Title <span class="text-red-500">*</span></label>
          <input v-model="form.dataset_title" type="text" placeholder="e.g. CAR-T Viability Assay"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Assessed By</label>
          <input v-model="form.assessed_by" type="text" placeholder="Your name"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
          <input v-model="form.notes" type="text" placeholder="Optional context"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button @click="startAssessment" :disabled="creating || !form.dataset_id || !form.dataset_title"
          class="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
          {{ creating ? 'Creating…' : 'Start Assessment →' }}
        </button>
      </div>
    </div>

    <!-- Error state -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-sm text-red-700">
      {{ error }}
    </div>

    <!-- Past assessments -->
    <div v-if="assessments.length">
      <h2 class="text-lg font-semibold text-gray-800 mb-3">Previous Assessments</h2>
      <div class="space-y-3">
        <div v-for="a in assessments" :key="a.id"
          class="bg-white border border-gray-200 rounded-xl p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
          <!-- Score -->
          <div class="text-center min-w-[56px]">
            <div :class="['text-2xl font-bold', scoreColor(a.overall_score)]">{{ a.overall_score }}%</div>
            <div class="text-xs text-gray-400">overall</div>
          </div>
          <!-- Principle bars -->
          <div class="flex-1 grid grid-cols-4 gap-2">
            <div v-for="[p, score, color] in [['F', a.f_score, 'bg-blue-500'], ['A', a.a_score, 'bg-emerald-500'], ['I', a.i_score, 'bg-violet-500'], ['R', a.r_score, 'bg-amber-500']]" :key="p">
              <div class="text-xs text-gray-500 mb-1">{{ p }} {{ score }}%</div>
              <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div :class="[color, 'h-full rounded-full transition-all']" :style="`width:${score}%`"></div>
              </div>
            </div>
          </div>
          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="font-medium text-gray-900 truncate">{{ a.dataset_title }}</div>
            <div class="text-xs text-gray-400">{{ a.dataset_id }} · {{ a.assessed_by || 'unknown' }}</div>
          </div>
          <!-- Actions -->
          <div class="flex gap-2 shrink-0">
            <router-link :to="`/assess/${a.id}`"
              class="text-sm px-3 py-1.5 border border-indigo-300 text-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors">
              Edit
            </router-link>
            <router-link :to="`/result/${a.id}`"
              class="text-sm px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
              Results
            </router-link>
            <button @click="removeAssessment(a.id)"
              class="text-sm px-2 py-1.5 text-red-400 hover:text-red-600 transition-colors" title="Delete">
              ✕
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!loading && !error" class="text-center text-gray-400 py-10 text-sm">
      No assessments yet. Start one above.
    </div>
  </div>
</template>
