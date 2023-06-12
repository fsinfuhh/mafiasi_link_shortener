import type { Link } from "@/api";
import { defineStore } from "pinia";

export const useLinkStore = defineStore("shortlinks", {
  state: () => ({
    links: [] as Link[],
  }),
  getters: {
    byId: (state) => (short: string) => state.links.find((iLink) => (iLink._short = short)),
  },
  actions: {
    delete(short: string) {
      this.links = this.links.filter((iLink) => iLink._short !== short);
    },
    add(link: Link) {
      this.links.push(link);
    },
    update(short: string, newData: Partial<Link>) {
      this.links = this.links.map((iLink) => {
        if (iLink._short === short) {
          return Object.assign(iLink, newData);
        } else {
          return iLink;
        }
      });
    },
  },
});

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
  }),
});
