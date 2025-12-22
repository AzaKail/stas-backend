import { defineStore } from "pinia";
import { api } from "../api";

export const useCatalogStore = defineStore("catalog", {
  state: () => ({
    categories: [],
    filtersMeta: { memories: [], colors: [], tags: [], price: { min: 0, max: 0 } },

    items: [],
    count: 0,
    page: 1,
    pageSize: 12,

    // текущие фильтры
    q: "",
    category: "",    // slug
    brand: "",
    memories: [],    // [256,512]
    colors: [],      // ["Midnight"...]
    tags: [],        // ["esim"...] (slug)
    priceMin: null,
    priceMax: null,

    loading: false,
  }),

  actions: {
    async loadCategories() {
      // если есть ручка /categories/
      try {
        const res = await api.get("categories/");
        this.categories = res.data;
      } catch {
        // fallback: если categories нет — попробуем взять из filters
        const res = await api.get("filters/");
        const cats = res.data.categories || [];
        // если бэк отдаёт просто строки — преобразуем в {slug,title}
        this.categories = cats.map((c) =>
          typeof c === "string" ? { slug: c.toLowerCase(), title: c } : c
        );
      }
    },

    async loadFiltersMeta() {
      const params = {};
      if (this.category) params.category = this.category;
      if (this.brand) params.brand = this.brand;

      const res = await api.get("filters/", { params });
      // ожидаем формат:
      // { memories:[], colors:[], tags:[], price:{min,max}, brands:[], categories:[] }
      this.filtersMeta = {
        memories: res.data.memories || [],
        colors: res.data.colors || [],
        tags: res.data.tags || [],
        price: res.data.price || { min: 0, max: 0 },
      };

      // если не задано, подхватим диапазон цен
      if (this.priceMin === null) this.priceMin = this.filtersMeta.price.min;
      if (this.priceMax === null) this.priceMax = this.filtersMeta.price.max;
    },

    async loadProducts() {
      this.loading = true;
      try {
        const params = {
          page: this.page,
          q: this.q || undefined,
          category: this.category || undefined,
          brand: this.brand || undefined,
          price_min: this.priceMin ?? undefined,
          price_max: this.priceMax ?? undefined,
        };

        // мульти-параметры
        (this.memories || []).forEach((m) => (params.memory = params.memory ? [].concat(params.memory, m) : [m]));
        (this.colors || []).forEach((c) => (params.color = params.color ? [].concat(params.color, c) : [c]));
        (this.tags || []).forEach((t) => (params.tag = params.tag ? [].concat(params.tag, t) : [t]));

        const res = await api.get("products/", { params });

        // DRF pagination обычно: {count, next, previous, results}
        this.items = res.data.results ?? res.data;
        this.count = res.data.count ?? this.items.length;
      } finally {
        this.loading = false;
      }
    },

    resetFilters() {
      this.q = "";
      this.brand = "";
      this.memories = [];
      this.colors = [];
      this.tags = [];
      this.priceMin = this.filtersMeta.price.min;
      this.priceMax = this.filtersMeta.price.max;
      this.page = 1;
    },
  },
});
