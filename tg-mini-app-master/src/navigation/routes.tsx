import { Boost, Clans, ErrorPage, Fellows, League, Main, Squad, Tasks } from "@/pages"
import type { ComponentType, JSX } from 'react'

interface Route {
  path: string;
  Component: ComponentType;
  title?: string;
  icon?: JSX.Element;
}

export const routes: Route[] = [
  { path: '/error', Component: ErrorPage },
  { path: '/', Component: Main },
  { path: '/fellows', Component: Fellows },
  { path: '/boost', Component: Boost },
  { path: '/tasks', Component: Tasks },
  { path: '/clans', Component: Clans },
  { path: '/clans/:id', Component: Squad },
  { path: '/league', Component: League }
];
