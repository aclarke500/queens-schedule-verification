declare module 'vue-router' {
  import type { DefineComponent } from 'vue'
  
  export interface RouteMeta {
    title?: string;
    [key: string]: any;
  }

  export interface RouteLocationNormalized {
    path: string;
    name?: string | null;
    meta: RouteMeta;
    params: Record<string, string>;
    query: Record<string, string>;
    hash: string;
    matched: RouteRecord[];
    [key: string]: any;
  }

  export interface RouteRecord {
    path: string;
    components: Record<string, DefineComponent>;
    meta: RouteMeta;
    [key: string]: any;
  }

  export type NavigationGuardNext = (to?: any) => void;

  export function createRouter(options: any): any;
  export function createWebHistory(base?: string): any;
  export function useRouter(): any;
  export function useRoute(): RouteLocationNormalized;
} 