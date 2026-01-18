<template>
  <div class="drawer" :class="{ open }" @click.self="$emit('close')">
    <div class="drawer__panel">
      <div class="drawer__head">
        <div class="drawer__title">Фильтры</div>
        <button class="icon-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="filter-block">
        <div class="label">Память</div>
        <label v-for="m in meta.memories" :key="m" class="check">
          <input type="checkbox" :value="m" v-model="local.memories" />
          <span>{{ m }}GB</span>
        </label>
      </div>

      <div class="filter-block">
        <div class="label">Цвет</div>
        <label v-for="c in meta.colors" :key="c" class="check">
          <input type="checkbox" :value="c" v-model="local.colors" />
          <span>{{ c }}</span>
        </label>
      </div>

      <div class="filter-block" v-if="tagGroups.length">
        <div class="label">Тэги</div>
        <div v-for="group in tagGroups" :key="group.title" class="tag-group">
          <div class="label muted">{{ group.title }}</div>
          <label v-for="t in group.items" :key="t.slug || t" class="check">
            <input type="checkbox" :value="t.slug || t" v-model="local.tags" />
            <span>{{ t.title || t }}</span>
          </label>
        </div>
      </div>

      <div class="filter-block">
        <div class="label">Цена</div>
        <div class="row">
          <input class="input" type="number" :min="meta.price.min" :max="meta.price.max" v-model.number="local.priceMin" />
          <input class="input" type="number" :min="meta.price.min" :max="meta.price.max" v-model.number="local.priceMax" />
        </div>
        <input
          class="range"
          type="range"
          :min="meta.price.min"
          :max="meta.price.max"
          v-model.number="local.priceMin"
          @input="syncPriceRange('min')"
        />
        <input
          class="range"
          type="range"
          :min="meta.price.min"
          :max="meta.price.max"
          v-model.number="local.priceMax"
          @input="syncPriceRange('max')"
        />
      </div>

      <div class="drawer__actions">
        <button class="btn" @click="apply">Применить</button>
        <button class="btn btn--ghost" @click="reset">Сбросить</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, watch } from "vue";

const props = defineProps({
  open: Boolean,
  meta: { type: Object, required: true },
  value: { type: Object, required: true }, // текущие значения из store
});

const emit = defineEmits(["close", "apply", "reset"]);

const local = reactive({
  memories: [],
  colors: [],
  tags: [],
  priceMin: 0,
  priceMax: 0,
});

const tagGroups = computed(() => {
  const groups = new Map();
  (props.meta.tags || []).forEach((tag) => {
    const normalized = typeof tag === "string" ? { slug: tag, title: tag, group: "Прочее" } : tag;
    const group = normalized.group || "Прочее";
    if (!groups.has(group)) groups.set(group, []);
    groups.get(group).push(normalized);
  });
  return Array.from(groups.entries()).map(([title, items]) => ({ title, items }));
});

watch(
  () => props.value,
  (v) => {
    local.memories = [...(v.memories || [])];
    local.colors = [...(v.colors || [])];
    local.tags = [...(v.tags || [])];
    local.priceMin = v.priceMin ?? props.meta.price.min;
    local.priceMax = v.priceMax ?? props.meta.price.max;
  },
  { immediate: true, deep: true }
);

function clampPrice(value) {
  const min = props.meta.price.min ?? 0;
  const max = props.meta.price.max ?? 0;
  return Math.min(Math.max(value, min), max);
}

function syncPriceRange(changed) {
  local.priceMin = clampPrice(local.priceMin ?? props.meta.price.min);
  local.priceMax = clampPrice(local.priceMax ?? props.meta.price.max);
  if (local.priceMin > local.priceMax) {
    if (changed === "min") {
      local.priceMax = local.priceMin;
    } else if (changed === "max") {
      local.priceMin = local.priceMax;
    } else {
      const temp = local.priceMin;
      local.priceMin = local.priceMax;
      local.priceMax = temp;
    }
  }
}
function apply() {
  emit("apply", { ...local });
  emit("close");
}
function reset() {
  emit("reset");
}
</script>
