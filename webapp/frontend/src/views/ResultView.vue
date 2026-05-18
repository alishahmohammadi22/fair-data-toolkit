<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAssessment } from '../api/client.js'
import ScoreGauge from '../components/ScoreGauge.vue'

const route = useRoute()
const router = useRouter()
const assessment = ref(null)

const PRINCIPLE_META = {
  F: { label: 'Findable',       color: '#3B82F6', bg: 'bg-blue-50',    border: 'border-blue-200',   text: 'text-blue-700' },
  A: { label: 'Accessible',     color: '#10B981', bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-700' },
  I: { label: 'Interoperable',  color: '#8B5CF6', bg: 'bg-violet-50',  border: 'border-violet-200',  text: 'text-violet-700' },
  R: { label: 'Reusable',       color: '#F59E0B', bg: 'bg-amber-50',   border: 'border-amber-200',   text: 'text-amber-700' },
}

const overallColor = (score) => {
  if (score >= 70) return '#10B981'
  if (score >= 40) return '#F59E0B'
  return '#EF4444'
}

onMounted(async () => {
  const res = await getAssessment(route.params.id)
  assessment.value = res.data
})
</script>

<template>
  <div v-if="assessment" class="max-w-5xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8 flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ assessment.dataset_title }}</h1>
        <p class="text-sm text-gray-500 mt-0.5">{{ assessment.dataset_id }} · {{ assessment.assessed_by }}</p>
      </div>
      <button @click="router.push(`/assess/${assessment.id}`)"
        class="text-sm px-4 py-2 border border-indigo-300 text-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors">
        ← Edit Assessment
      </button>
    </div>

    <!-- Score gauges -->
    <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 mb-6">
      <h2 class="text-base font-semibold text-gray-700 mb-6">FAIR Score Overview</h2>
      <div class="flex flex-wrap justify-around gap-6">
        <ScoreGauge :score="assessment.overall_score" label="Overall" :color="overallColor(assessment.overall_score)" :size="130" />
        <ScoreGauge :score="assessment.f_score" label="Findable"      color="#3B82F6" />
        <ScoreGauge :score="assessment.a_score" label="Accessible"    color="#10B981" />
        <ScoreGauge :score="assessment.i_score" label="Interoperable" color="#8B5CF6" />
        <ScoreGauge :score="assessment.r_score" label="Reusable"      color="#F59E0B" />
      </div>
    </div>

    <!-- Interpretation -->
    <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 mb-6">
      <div v-for="[p, scoreKey] in [['F','f_score'],['A','a_score'],['I','i_score'],['R','r_score']]" :key="p"
        :class="['rounded-xl border p-4', PRINCIPLE_META[p].bg, PRINCIPLE_META[p].border]">
        <div :class="['text-3xl font-bold', PRINCIPLE_META[p].text]">{{ assessment[scoreKey] }}%</div>
        <div class="text-sm font-medium text-gray-600 mt-1">{{ PRINCIPLE_META[p].label }}</div>
        <div class="mt-2 h-1.5 bg-white/60 rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all" :style="`width:${assessment[scoreKey]}%; background:${PRINCIPLE_META[p].color}`"></div>
        </div>
      </div>
    </div>

    <!-- Essential gaps -->
    <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 mb-6">
      <h2 class="text-base font-semibold text-gray-700 mb-4">
        Essential Gaps
        <span class="ml-2 text-sm font-normal text-red-500 bg-red-50 px-2 py-0.5 rounded-full">
          {{ assessment.essential_gaps?.length ?? 0 }} unmet
        </span>
      </h2>
      <div v-if="assessment.essential_gaps?.length" class="space-y-2">
        <div v-for="gap in assessment.essential_gaps" :key="gap.indicator_id"
          class="flex items-start gap-3 p-3 bg-red-50 border border-red-100 rounded-lg">
          <span class="text-red-500 text-lg leading-none mt-0.5">✗</span>
          <div>
            <span :class="['text-xs font-bold px-1.5 py-0.5 rounded mr-2', PRINCIPLE_META[gap.principle]?.text, PRINCIPLE_META[gap.principle]?.bg]">
              {{ gap.indicator_id }}
            </span>
            <span class="text-sm text-gray-700">{{ gap.indicator_name }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-emerald-600 font-medium text-sm">
        ✓ All essential indicators are compliant.
      </div>
    </div>

    <!-- All scores table -->
    <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
      <h2 class="text-base font-semibold text-gray-700 mb-4">All Indicator Scores</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-100 text-left text-xs text-gray-500 uppercase tracking-wide">
              <th class="pb-2 pr-4">ID</th>
              <th class="pb-2 pr-4">Compliance</th>
              <th class="pb-2">Evidence</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in assessment.scores" :key="s.indicator_id"
              class="border-b border-gray-50 hover:bg-gray-50">
              <td class="py-2 pr-4 font-mono text-xs text-gray-600">{{ s.indicator_id }}</td>
              <td class="py-2 pr-4">
                <span :class="[
                  'text-xs px-2 py-0.5 rounded-full font-medium',
                  s.compliance === 'compliant'           ? 'bg-emerald-100 text-emerald-700' :
                  s.compliance === 'partially_compliant' ? 'bg-yellow-100 text-yellow-700' :
                  s.compliance === 'not_compliant'       ? 'bg-red-100 text-red-700' :
                  s.compliance === 'not_applicable'      ? 'bg-gray-100 text-gray-500' :
                                                           'bg-gray-100 text-gray-400'
                ]">
                  {{ s.compliance.replace(/_/g, ' ') }}
                </span>
              </td>
              <td class="py-2 text-xs text-gray-500 max-w-xs truncate">{{ s.evidence || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div v-else class="text-center text-gray-400 py-20">Loading results…</div>
</template>
