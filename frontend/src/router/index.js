import { createRouter, createWebHistory } from "vue-router";
import CatalogPage from "../pages/CatalogPage.vue";
import ProductPage from "../pages/ProductPage.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/catalog" },
    { path: "/catalog", component: CatalogPage },
    { path: "/product/:slug", component: ProductPage, props: true },
  ],
});
