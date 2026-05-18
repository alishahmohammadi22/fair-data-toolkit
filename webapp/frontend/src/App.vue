<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navbar -->
    <nav class="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4 shadow-sm">
      <router-link to="/" class="flex items-center gap-2">
        <span class="text-2xl">⚖️</span>
        <span class="font-bold text-lg text-indigo-700 tracking-tight">FAIR Toolkit</span>
      </router-link>
      <span class="text-gray-300">|</span>
      <span class="text-sm text-gray-500">FAIR Data Maturity Assessment</span>
      <div class="ml-auto flex gap-2 text-xs">
        <span class="px-2 py-1 rounded-full bg-blue-100 text-blue-700 font-medium">F</span>
        <span class="px-2 py-1 rounded-full bg-emerald-100 text-emerald-700 font-medium">A</span>
        <span class="px-2 py-1 rounded-full bg-violet-100 text-violet-700 font-medium">I</span>
        <span class="px-2 py-1 rounded-full bg-amber-100 text-amber-700 font-medium">R</span>
      </div>
    </nav>

    <!-- Page content -->
    <main class="flex-1">
      <router-view />
    </main>

    <footer class="text-center text-xs text-gray-400 py-4 border-t border-gray-100">
      FAIR Data Toolkit v0.1.0 · RDA FAIR Maturity Model (2020) · 38 Indicators
    </footer>
  </div>
</template>
