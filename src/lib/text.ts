import type {Catalog} from '../types';

/** Lowercase without accents, so "Pokemon" finds "Pokémon". */
export const normalize = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();

/**
 * Free space the complete library needs, in whole GB with a small margin: on the storage, and on a
 * computer that holds the ZIP and its extracted copy at the same time.
 */
export function librarySpace(catalog: Catalog) {
  const gb = ((catalog.imageBytes + catalog.globalManifestBytes) * 1.05) / 1e9;
  return {storage: Math.ceil(gb), local: Math.ceil(gb * 2)};
}

/**
 * Fills the library figures into the written guide and help texts, so they follow the catalog:
 * {packs}, {folders}, {jsons}, {storage} and {local}.
 */
export function fillCounts(text: string, catalog: Catalog) {
  const space = librarySpace(catalog);
  const values: Record<string, string> = {
    packs: String(catalog.packCount),
    folders: String(catalog.packCount),
    jsons: String(catalog.packCount + 1),
    storage: `${space.storage} GB`,
    local: `${space.local} GB`,
  };
  return text.replace(/\{(\w+)\}/g, (all, key: string) => values[key] ?? all);
}
