CONFLICTS = {
    "silk_touch": {"fortune"},
    "fortune": {"silk_touch"},
    "sharpness": {"smite", "bane_of_arthropods"},
    "smite": {"sharpness", "bane_of_arthropods"},
    "bane_of_arthropods": {"sharpness", "smite"},
    "protection": {"fire_protection", "blast_protection", "projectile_protection"},
    "fire_protection": {"protection", "blast_protection", "projectile_protection"},
    "blast_protection": {"protection", "fire_protection", "projectile_protection"},
    "projectile_protection": {"protection", "fire_protection", "blast_protection"},
    "depth_strider": {"frost_walker"},
    "frost_walker": {"depth_strider"},
    "multishot": {"piercing"},
    "piercing": {"multishot"},
    "riptide": {"channeling", "loyalty"},
    "channeling": {"riptide"},
    "loyalty": {"riptide"},
}

def detect_conflicts(selected_ids):
    conflicts = []
    selected = set(selected_ids)

    for ench in selected:
        if ench in CONFLICTS:
            for bad in CONFLICTS[ench]:
                if bad in selected:
                    conflicts.append(tuple(sorted((ench, bad))))

    # Deduplicate
    return list(dict.fromkeys(conflicts))
