<script setup>
import { ref } from 'vue'

const props = defineProps({
  indicator: { type: Object, required: true },
  score: { type: Object, required: true },
})
const emit = defineEmits(['update:score'])

const expanded = ref(false)

const COMPLIANCE_OPTIONS = [
  { value: 'not_assessed',       label: 'Not Assessed' },
  { value: 'not_applicable',     label: 'Not Applicable' },
  { value: 'not_compliant',      label: 'Not Compliant' },
  { value: 'partially_compliant',label: 'Partially Compliant' },
  { value: 'compliant',          label: 'Compliant' },
]

const PRIORITY_STYLES = {
  essential:  'bg-red-100 text-red-700',
  important:  'bg-yellow-100 text-yellow-700',
  useful:     'bg-green-100 text-green-700',
}

const SCOPE_STYLES = {
  data:     'bg-blue-50 text-blue-600 border-blue-200',
  metadata: 'bg-purple-50 text-purple-600 border-purple-200',
}

const COMPLIANCE_BORDER = {
  compliant:           'border-emerald-400 bg-emerald-50/30',
  partially_compliant: 'border-yellow-400 bg-yellow-50/30',
  not_compliant:       'border-red-400 bg-red-50/30',
  not_applicable:      'border-gray-200 bg-gray-50/50',
  not_assessed:        'border-gray-200',
}

function update(field, value) {
  emit('update:score', { ...props.score, [field]: value })
}
</script>

<template>
  <div :class="['border rounded-xl p-4 transition-all', COMPLIANCE_BORDER[score.compliance] ?? 'border-gray-200']">
    <!-- Header row -->
    <div class="flex flex-wrap items-start gap-2 mb-2">
      <!-- ID -->
      <span class="font-mono text-xs font-bold text-gray-600 bg-gray-100 px-2 py-0.5 rounded">
        {{ indicator.id }}
      </span>
      <!-- Priority -->
      <span :class="['text-xs font-medium px-2 py-0.5 rounded-full', PRIORITY_STYLES[indicator.priority] ?? 'bg-gray-100 text-gray-500']">
        {{ indicator.priority }}
      </span>
      <!-- Scope -->
      <span :class="['text-xs border px-2 py-0.5 rounded-full', SCOPE_STYLES[indicator.scope] ?? 'border-gray-200 text-gray-500']">
        {{ indicator.scope }}
      </span>
      <!-- Expand toggle -->
      <button @click="expanded = !expanded" class="ml-auto text-xs text-gray-400 hover:text-gray-600">
        {{ expanded ? '▲ less' : '▼ details' }}
      </button>
    </div>

    <!-- Name -->
    <p class="text-sm font-medium text-gray-800 mb-2">{{ indicator.name }}</p>

    <!-- Question (collapsible) -->
    <transition name="slide">
      <div v-if="expanded" class="text-xs text-gray-500 bg-white/70 border border-gray-100 rounded p-3 mb-3 leading-relaxed">
        <strong class="text-gray-600">Question:</strong> {{ indicator.question }}
        <div v-if="indicator.description" class="mt-1">
          <strong class="text-gray-600">Guidance:</strong> {{ indicator.description }}
        </div>
      </div>
    </transition>

    <!-- Controls -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <!-- Compliance dropdown -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Compliance</label>
        <select
          :value="score.compliance"
          @change="update('compliance', $event.target.value)"
          class="w-full text-sm border border-gray-200 rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-white"
        >
          <option v-for="opt in COMPLIANCE_OPTIONS" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
      <!-- Evidence -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Evidence</label>
        <textarea
          :value="score.evidence"
          @input="update('evidence', $event.target.value)"
          rows="2"
          placeholder="Describe your evidence…"
          class="w-full text-sm border border-gray-200 rounded-lg px-2 py-1.5 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
      </div>
      <!-- Action notes -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Action Notes</label>
        <textarea
          :value="score.action_notes"
          @input="update('action_notes', $event.target.value)"
          rows="2"
          placeholder="Remediation steps…"
          class="w-full text-sm border border-gray-200 rounded-lg px-2 py-1.5 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: max-height 0.25s ease, opacity 0.25s; overflow: hidden; }
.slide-enter-from, .slide-leave-to { max-height: 0; opacity: 0; }
.slide-enter-to, .slide-leave-from { max-height: 300px; opacity: 1; }
</style>
