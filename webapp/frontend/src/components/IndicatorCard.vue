<script setup>
import { ref } from 'vue'

const props = defineProps({
  indicator: { type: Object, required: true },
  score: { type: Object, required: true },
})
const emit = defineEmits(['update:score'])

const expanded = ref(false)

const COMPLIANCE_OPTIONS = [
  { value: 'fully_implemented',     label: 'Fully Implemented'        },
  { value: 'in_implementation',     label: 'In Implementation Phase'  },
  { value: 'under_consideration',   label: 'Under Consideration'      },
  { value: 'not_being_considered',  label: 'Not Being Considered Yet' },
  { value: 'not_assessed',          label: 'Not Assessed'             },
  { value: 'not_applicable',        label: 'Not Applicable'           },
]

const PRIORITY_STYLES = {
  essential: 'bg-red-100 text-red-700',
  important: 'bg-yellow-100 text-yellow-700',
  useful:    'bg-green-100 text-green-700',
}

const SCOPE_STYLES = {
  data:     'bg-blue-50 text-blue-500',
  metadata: 'bg-purple-50 text-purple-500',
}

// Left border colour driven by compliance
const COMPLIANCE_BORDER = {
  fully_implemented:    'border-l-emerald-400',
  in_implementation:    'border-l-blue-400',
  under_consideration:  'border-l-yellow-400',
  not_being_considered: 'border-l-red-400',
  not_applicable:       'border-l-gray-300',
  not_assessed:         'border-l-gray-200',
}

const COMPLIANCE_ROW_BG = {
  fully_implemented:    'bg-emerald-50/40',
  in_implementation:    'bg-blue-50/40',
  under_consideration:  'bg-yellow-50/40',
  not_being_considered: 'bg-red-50/30',
  not_applicable:       'bg-gray-50/50',
  not_assessed:         '',
}

function update(field, value) {
  emit('update:score', { ...props.score, [field]: value })
}
</script>

<template>
  <div :class="[
    'border border-l-4 rounded-lg transition-all',
    COMPLIANCE_BORDER[score.compliance] ?? 'border-l-gray-200',
    COMPLIANCE_ROW_BG[score.compliance],
    expanded ? 'border-gray-300' : 'border-gray-100',
  ]">
    <!-- ── Compact always-visible row ── -->
    <div
      class="flex items-center gap-2 px-3 py-2 cursor-pointer select-none"
      @click="expanded = !expanded"
    >
      <!-- ID -->
      <span class="font-mono text-xs font-bold text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded shrink-0 w-32 text-center">
        {{ indicator.id }}
      </span>

      <!-- Priority dot -->
      <span :class="['text-xs font-semibold px-1.5 py-0.5 rounded shrink-0', PRIORITY_STYLES[indicator.priority]]">
        {{ indicator.priority[0].toUpperCase() }}
      </span>

      <!-- Scope -->
      <span :class="['text-xs px-1.5 py-0.5 rounded shrink-0', SCOPE_STYLES[indicator.scope] ?? 'text-gray-400']">
        {{ indicator.scope === 'data' ? 'D' : 'M' }}
      </span>

      <!-- Name -->
      <span class="text-sm text-gray-800 font-medium flex-1 truncate">{{ indicator.name }}</span>

      <!-- Compliance select — stop click from toggling expand -->
      <select
        :value="score.compliance"
        @change="update('compliance', $event.target.value)"
        @click.stop
        :class="[
          'text-xs border rounded px-2 py-1 shrink-0 w-44 focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-white',
          score.compliance === 'fully_implemented'    ? 'border-emerald-300 text-emerald-700' :
          score.compliance === 'in_implementation'     ? 'border-blue-300 text-blue-700' :
          score.compliance === 'under_consideration'   ? 'border-yellow-300 text-yellow-700' :
          score.compliance === 'not_being_considered'  ? 'border-red-300 text-red-700' :
                                                         'border-gray-200 text-gray-600'
        ]"
      >
        <option v-for="opt in COMPLIANCE_OPTIONS" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Chevron -->
      <svg :class="['w-4 h-4 text-gray-400 shrink-0 transition-transform', expanded ? 'rotate-180' : '']"
           fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <!-- ── Expanded detail panel ── -->
    <transition name="slide">
      <div v-if="expanded" class="px-3 pb-3 border-t border-gray-100">
        <!-- Question / guidance -->
        <p class="text-xs text-gray-500 mt-2 mb-3 leading-relaxed">
          <span class="font-semibold text-gray-600">Q: </span>{{ indicator.question }}
        </p>

        <!-- Evidence + action notes side by side -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Evidence</label>
            <textarea
              :value="score.evidence"
              @input="update('evidence', $event.target.value)"
              rows="2"
              placeholder="Describe your evidence…"
              class="w-full text-xs border border-gray-200 rounded px-2 py-1.5 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Action Notes</label>
            <textarea
              :value="score.action_notes"
              @input="update('action_notes', $event.target.value)"
              rows="2"
              placeholder="Remediation steps…"
              class="w-full text-xs border border-gray-200 rounded px-2 py-1.5 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: max-height 0.2s ease, opacity 0.15s;
  overflow: hidden;
}
.slide-enter-from, .slide-leave-to { max-height: 0; opacity: 0; }
.slide-enter-to, .slide-leave-from { max-height: 240px; opacity: 1; }
</style>
