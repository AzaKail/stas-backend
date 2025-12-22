<template>
  <div class="tabs">
    <button
      class="tab"
      :class="{ active: modelValue === '' }"
      @click="$emit('update:modelValue', '')"
    >
      Все
    </button>

    <button
      v-for="c in categories"
      :key="c.slug"
      class="tab"
      :class="{ active: modelValue === c.slug }"
      @click="$emit('update:modelValue', c.slug)"
    >
      {{ c.title }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  categories: { type: Array, default: () => [] },
  modelValue: { type: String, default: "" },
});
defineEmits(["update:modelValue"]);
</script>
