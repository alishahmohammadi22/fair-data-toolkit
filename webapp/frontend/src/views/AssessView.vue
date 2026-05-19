<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getIndicators, getAssessment, updateScores } from '../api/client.js'
import IndicatorCard from '../components/IndicatorCard.vue'

const route = useRoute()
const router = useRouter()
const assessmentId = route.params.id

const assessment = ref(null)
const indicators = ref([])
const activeTab = ref('F')
const saving = ref(false)
const saved = ref(false)

const PRINCIPLES = ['F', 'A', 'I', 'R']
const LABELS = { F: 'Findable', A: 'Accessible', I: 'Interoperable', R: 'Reusable' }
const TAB_COLORS = {
  F: { active: 'border-blue-500 text-blue-600', dot: 'bg-blue-500' },
  A: { active: 'border-emerald-500 text-emerald-600', dot: 'bg-emerald-500' },
  I: { active: 'border-violet-500 text-violet-600', dot: 'bg-violet-500' },
  R: { active: 'border-amber-500 text-amber-600', dot: 'bg-amber-500' },
}

// scores[indicator_id] = { compliance, evidence, action_notes }
const scores = reactive({})

const tabIndicators = computed(() =>
  indicators.value.filter(ind => ind.principle === activeTab.value)
)

function progressForTab(p) {
  const tabInds = indicators.value.filter(i => i.principle === p)
  if (!tabInds.length) return 0
  const assessed = tabInds.filter(
    i => scores[i.id]?.compliance && scores[i.id].compliance !== 'not_assessed'
  ).length
  return Math.round((assessed / tabInds.length) * 100)
}

onMounted(async () => {
  const [indRes, asmRes] = await Promise.all([
    getIndicators(),
    getAssessment(assessmentId),
  ])
  indicators.value = indRes.data
  assessment.value = asmRes.data

  // Initialise scores with existing values or defaults
  for (const ind of indRes.data) {
    const existing = asmRes.data.scores.find(s => s.indicator_id === ind.id)
    scores[ind.id] = {
      compliance: existing?.compliance ?? 'not_assessed',
      evidence: existing?.evidence ?? '',
      action_notes: existing?.action_notes ?? '',
    }
  }
})

let saveTimer = null
function scheduleAutoSave() {
  saved.value = false
  clearTimeout(saveTimer)
  saveTimer = setTimeout(flushSave, 1200)
}

async function flushSave() {
  saving.value = true
  const payload = Object.entries(scores).map(([indicator_id, s]) => ({
    indicator_id,
    compliance: s.compliance,
    evidence: s.evidence || null,
    action_notes: s.action_notes || null,
  }))
  await updateScores(assessmentId, payload)
  saving.value = false
  saved.value = true
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden" style="height: calc(100vh - 41px)">
    <!-- Header -->
    <div class="px-6 py-2 border-b border-gray-200 bg-white flex flex-wrap items-center justify-between gap-2 shrink-0">
      <div>
        <h1 class="text-base font-bold text-gray-900 leading-tight">{{ assessment?.dataset_title }}</h1>
        <p class="text-xs text-gray-400">
          {{ assessment?.dataset_id }}
          <span v-if="assessment?.assessed_by"> · {{ assessment.assessed_by }}</span>
        </p>
      </div>
      <div class="flex items-center gap-3">
        <transition name="fade">
          <span v-if="saving" class="text-xs text-gray-400">Saving…</span>
          <span v-else-if="saved" class="text-xs text-emerald-600 font-medium">✓ Saved</span>
        </transition>
        <button @click="router.push(`/result/${assessmentId}`)"
          class="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-indigo-700 transition-colors">
          View Results →
        </button>
      </div>
    </div>

    <!-- Principle tabs -->
    <div class="border-b border-gray-200 bg-white shrink-0">
      <nav class="flex px-6">
        <button
          v-for="p in PRINCIPLES"
          :key="p"
          @click="activeTab = p"
          :class="[
            'flex items-center gap-1.5 px-4 py-2 text-xs font-medium border-b-2 transition-colors',
            activeTab === p
              ? TAB_COLORS[p].active
              : 'border-transparent text-gray-500 hover:text-gray-700',
          ]"
        >
          <span :class="['w-2 h-2 rounded-full shrink-0', TAB_COLORS[p].dot]"></span>
          <span class="font-semibold">{{ p }}</span>
          <span class="hidden sm:inline opacity-70">{{ LABELS[p] }}</span>
          <span class="bg-gray-100 text-gray-600 rounded-full px-1.5 py-0.5">
            {{ progressForTab(p) }}%
          </span>
        </button>
      </nav>
    </div>

    <!-- Scrollable indicator list -->
    <div class="flex-1 overflow-y-auto px-6 py-2">
      <div v-if="tabIndicators.length && Object.keys(scores).length" class="space-y-1">
        <IndicatorCard
          v-for="ind in tabIndicators"
          :key="ind.id"
          :indicator="ind"
          :score="scores[ind.id]"
          @update:score="val => { Object.assign(scores[ind.id], val); scheduleAutoSave() }"
        />
      </div>
      <div v-else class="text-center text-gray-400 py-10 text-sm">Loading indicators…</div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
