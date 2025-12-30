import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import CatalogPage from "../pages/CatalogPage.vue";
import ProductPage from "../pages/ProductPage.vue";
import AboutPage from "../pages/AboutPage.vue";
import SellPage from "../pages/SellPage.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomePage },
    { path: "/catalog", component: CatalogPage },
    { path: "/product/:slug", component: ProductPage, props: true },
    { path: "/about", component: AboutPage },
    { path: "/sell", component: SellPage },
  ],
});
