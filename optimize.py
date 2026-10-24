# -*- coding: utf-8 -*-
"""Apply all audit optimizations to index.html for Marifer Delicias."""

DOMAIN = "https://mariferdelicias.cl"

with open('index.html', 'r', encoding='utf-8', newline='') as f:
    content = f.read()

NL = '\r\n' if '\r\n' in content else '\n'
original_len = len(content)

changes = []

# ============================================================
# 1. REMOVE giant favicon (P01) - Critical
# ============================================================
old = '    <link rel="shortcut icon" href="images/favico.png">' + NL
new = ''
if old in content:
    content = content.replace(old, new, 1)
    changes.append('✅ P01: Eliminado favico.png de 2.62MB')
else:
    changes.append('⚠️  P01: favico.png ya eliminado o no encontrado')

# ============================================================
# 2. ADD meta SEO + OG + canonical + theme-color + manifest (S01-S03, S07)
# ============================================================
google_fonts_line = '    <!-- Google Fonts -->'
meta_block = (
    '    <!-- SEO y metadatos sociales -->' + NL +
    '    <meta name="description" content="Marifer Delicias — Emprendimiento familiar en Los Ángeles, Chile. Granizados, helados soft, churros rellenos, calzones rotos y queques caseros. ¡Visítanos en la Feria de Las Pulgas!">' + NL +
    '    <meta name="theme-color" content="#0aabf1">' + NL +
    '    <link rel="canonical" href="' + DOMAIN + '/">' + NL +
    '    <link rel="manifest" href="manifest.json">' + NL +
    '    <!-- Open Graph / WhatsApp / Facebook -->' + NL +
    '    <meta property="og:type" content="website">' + NL +
    '    <meta property="og:url" content="' + DOMAIN + '/">' + NL +
    '    <meta property="og:locale" content="es_CL">' + NL +
    '    <meta property="og:title" content="Marifer Delicias | Emprendimiento Familiar en Los Ángeles">' + NL +
    '    <meta property="og:description" content="Granizados, helados soft, churros rellenos, calzones rotos y queques caseros. Encuéntranos en la Feria de Las Pulgas, Los Ángeles, Chile.">' + NL +
    '    <meta property="og:image" content="' + DOMAIN + '/images/carro-frontal.jpeg">' + NL +
    '    <meta property="og:image:width" content="1280">' + NL +
    '    <meta property="og:image:height" content="961">' + NL +
    '    <!-- Twitter/X Card -->' + NL +
    '    <meta name="twitter:card" content="summary_large_image">' + NL +
    '    <meta name="twitter:title" content="Marifer Delicias | Emprendimiento Familiar en Los Ángeles">' + NL +
    '    <meta name="twitter:description" content="Granizados, helados soft, churros, calzones rotos y queques caseros en Los Ángeles, Chile.">' + NL +
    '    <meta name="twitter:image" content="' + DOMAIN + '/images/carro-frontal.jpeg">' + NL
)
if google_fonts_line in content:
    content = content.replace(google_fonts_line, meta_block + google_fonts_line, 1)
    changes.append('✅ S01-S03, S07: Meta description, OG, canonical, theme-color, manifest')
else:
    changes.append('⚠️  SEO: Marcador Google Fonts no encontrado')

# ============================================================
# 3. NON-BLOCKING Google Fonts (P04) — preload trick
# ============================================================
old_fonts = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">' + NL +
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' + NL +
    '    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
)
new_fonts = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">' + NL +
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' + NL +
    '    <!-- Carga no bloqueante de fuentes (elimina Poppins 300 sin uso) -->' + NL +
    '    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Poppins:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel=\'stylesheet\'">' + NL +
    '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Poppins:wght@400;500;600;700&display=swap"></noscript>'
)
if old_fonts in content:
    content = content.replace(old_fonts, new_fonts, 1)
    changes.append('✅ P04: Google Fonts carga no bloqueante (Poppins 300 eliminado)')
else:
    changes.append('⚠️  P04: Bloque de Fonts no encontrado exactamente')

# ============================================================
# 4. PRELOAD hero background image (P05)
# ============================================================
preload_hero = '    <link rel="preload" as="image" href="images/carro-plaza-fondo.jpeg">' + NL
if 'rel="preload" as="image"' not in content:
    content = content.replace('<style>' + NL, preload_hero + '<style>' + NL, 1)
    changes.append('✅ P05: Preload imagen de fondo del hero')
else:
    changes.append('⚠️  P05: Preload ya existe')

# ============================================================
# 5. Schema.org JSON-LD LocalBusiness (S04)
# ============================================================
schema = (
    NL +
    '    <!-- Schema.org JSON-LD: LocalBusiness / FoodEstablishment para rich results Google -->' + NL +
    '    <script type="application/ld+json">' + NL +
    '    {' + NL +
    '      "@context": "https://schema.org",' + NL +
    '      "@type": ["FoodEstablishment", "LocalBusiness"],' + NL +
    '      "name": "Marifer Delicias",' + NL +
    '      "description": "Emprendimiento familiar de granizados, helados soft, churros rellenos, calzones rotos y queques caseros en Los Ángeles, Chile.",' + NL +
    '      "url": "' + DOMAIN + '",' + NL +
    '      "logo": "' + DOMAIN + '/images/logo.jpeg",' + NL +
    '      "image": "' + DOMAIN + '/images/carro-frontal.jpeg",' + NL +
    '      "address": {' + NL +
    '        "@type": "PostalAddress",' + NL +
    '        "streetAddress": "Feria de Las Pulgas",' + NL +
    '        "addressLocality": "Los Ángeles",' + NL +
    '        "addressRegion": "Región del Biobío",' + NL +
    '        "addressCountry": "CL"' + NL +
    '      },' + NL +
    '      "telephone": "+56950691959",' + NL +
    '      "sameAs": ["https://www.instagram.com/marifer_delicias/"],' + NL +
    '      "servesCuisine": ["Granizados", "Helados", "Churros", "Repostería chilena"],' + NL +
    '      "priceRange": "$",' + NL +
    '      "openingHours": "Sa-Su"' + NL +
    '    }' + NL +
    '    </script>'
)
if 'application/ld+json' not in content:
    content = content.replace('</head>', schema + NL + '</head>', 1)
    changes.append('✅ S04: Schema.org JSON-LD LocalBusiness/FoodEstablishment')
else:
    changes.append('⚠️  S04: JSON-LD ya existe')

# ============================================================
# 6. SKIP NAVIGATION CSS (A01) — add to style block
# ============================================================
skip_css = (
    '        /* --- SKIP NAVIGATION (accesibilidad teclado) --- */' + NL +
    '        .skip-link {' + NL +
    '            position: absolute;' + NL +
    '            left: -9999px;' + NL +
    '            top: 8px;' + NL +
    '            background: var(--celeste-neon);' + NL +
    '            color: var(--blue-deep);' + NL +
    '            padding: 8px 20px;' + NL +
    '            border-radius: 6px;' + NL +
    '            font-weight: 700;' + NL +
    '            font-size: 0.95rem;' + NL +
    '            z-index: 9999;' + NL +
    '            text-decoration: none;' + NL +
    '        }' + NL +
    '        .skip-link:focus {' + NL +
    '            left: 8px;' + NL +
    '        }' + NL + NL
)
style_open = '<style>' + NL
if '.skip-link' not in content:
    content = content.replace(style_open, style_open + skip_css, 1)
    changes.append('✅ A01: CSS skip-navigation agregado')

# ============================================================
# 7. SCROLL-BEHAVIOR with prefers-reduced-motion (P09)
# ============================================================
old_scroll = (
    '        html {' + NL +
    '            scroll-behavior: smooth;' + NL +
    '        }'
)
new_scroll = (
    '        @media (prefers-reduced-motion: no-preference) {' + NL +
    '            html {' + NL +
    '                scroll-behavior: smooth;' + NL +
    '            }' + NL +
    '        }'
)
if old_scroll in content:
    content = content.replace(old_scroll, new_scroll, 1)
    changes.append('✅ P09: scroll-behavior respeta prefers-reduced-motion')
else:
    changes.append('⚠️  P09: scroll-behavior no encontrado con ese formato')

# ============================================================
# 8. FIX outline: none in form inputs (A02)
# ============================================================
old_focus = (
    '            outline: none;' + NL +
    '            border-color: var(--celeste-neon);' + NL +
    '            box-shadow: 0 0 0 3px rgba(10, 171, 241, 0.25);'
)
new_focus = (
    '            outline: 3px solid var(--celeste-neon);' + NL +
    '            outline-offset: 2px;' + NL +
    '            border-color: var(--celeste-neon);' + NL +
    '            box-shadow: 0 0 0 4px rgba(10, 171, 241, 0.25);'
)
if old_focus in content:
    content = content.replace(old_focus, new_focus, 1)
    changes.append('✅ A02: Foco de formularios visible (WCAG 2.2)')
else:
    changes.append('⚠️  A02: Bloque de outline no encontrado exactamente')

# ============================================================
# 9. ADD PRINT STYLES (UX02)
# ============================================================
print_css = (
    NL +
    '        /* --- PRINT STYLES --- */' + NL +
    '        @media print {' + NL +
    '            body { background: white !important; color: black !important; }' + NL +
    '            .site-header, .carousel-nav-btn, .carousel-dots,' + NL +
    '            .whatsapp-cta, .mobile-toggle, .nav-menu { display: none !important; }' + NL +
    '            .brand-text h1 { color: #001f54 !important; }' + NL +
    '            .section-title { color: #0042b0 !important; }' + NL +
    '            a { text-decoration: none; color: inherit; }' + NL +
    '        }'
)
if '@media print' not in content:
    content = content.replace('    </style>', print_css + NL + '    </style>', 1)
    changes.append('✅ UX02: Estilos de impresión (print media query)')
else:
    changes.append('⚠️  UX02: @media print ya existe')

# ============================================================
# 10. SKIP LINK HTML element (A01) — first thing in <body>
# ============================================================
skip_html = '<a href="#quienes-somos" class="skip-link">Saltar al contenido principal</a>' + NL + NL
body_tag = '<body>' + NL
if 'skip-link' not in content or 'href="#quienes-somos" class="skip-link"' not in content:
    content = content.replace(body_tag, body_tag + skip_html, 1)
    changes.append('✅ A01: Skip link HTML insertado al inicio del body')

# ============================================================
# 11. WRAP nav in <nav> with aria-label (A03)
# ============================================================
old_nav_comment = '            <!-- Menú informativo con enlace oficial a Instagram -->'
old_nav_ul = '            <ul class="nav-menu" id="navMenu">'
new_nav = (
    '            <!-- Menú informativo con enlace oficial a Instagram -->' + NL +
    '            <nav aria-label="Navegación principal">' + NL +
    '            <ul class="nav-menu" id="navMenu">'
)
close_ul = '            </ul>'
close_ul_new = '            </ul>' + NL + '            </nav>'

if '<nav aria-label="Navegación principal">' not in content:
    content = content.replace(
        old_nav_comment + NL + old_nav_ul,
        new_nav,
        1
    )
    # Close the nav — find the closing ul near the navMenu
    content = content.replace(
        '            </ul>' + NL + '        </div>' + NL + '    </header>',
        '            </ul>' + NL + '            </nav>' + NL + '        </div>' + NL + '    </header>',
        1
    )
    changes.append('✅ A03: Menú envuelto en <nav aria-label>')
else:
    changes.append('⚠️  A03: <nav> ya existe')

# ============================================================
# 12. FIX window.open security (SEC01)
# ============================================================
old_open = "window.open(whatsappUrl, '_blank');"
new_open = "window.open(whatsappUrl, '_blank', 'noopener,noreferrer');"
if old_open in content:
    content = content.replace(old_open, new_open, 1)
    changes.append('✅ SEC01: window.open con noopener,noreferrer')
else:
    changes.append('⚠️  SEC01: window.open no encontrado')

# ============================================================
# 13. ADD loading="lazy" to non-hero images (P02)
# ============================================================
import re

# Images that should NOT have lazy (first-viewport items)
no_lazy = ['logo.jpeg', 'carro-plaza-fondo.jpeg']

def add_lazy(m):
    tag = m.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    if not src_match:
        return tag
    src = src_match.group(1)
    if any(nl in src for nl in no_lazy):
        return tag
    if 'loading=' in tag:
        return tag
    # Insert loading="lazy" before the closing >
    return tag[:-1] + ' loading="lazy">'

content = re.sub(r'<img [^>]+>', add_lazy, content)
changes.append('✅ P02: loading="lazy" en imágenes fuera del primer viewport')

# ============================================================
# 14. ADD aria-expanded to mobile toggle (A04)
# ============================================================
old_toggle_html = '<button class="mobile-toggle" id="menuToggle" aria-label="Abrir navegación">☰</button>'
new_toggle_html = '<button class="mobile-toggle" id="menuToggle" aria-label="Abrir menú de navegación" aria-expanded="false" aria-controls="navMenu">☰</button>'
if old_toggle_html in content:
    content = content.replace(old_toggle_html, new_toggle_html, 1)
    changes.append('✅ A04: aria-expanded en botón hamburguesa')
else:
    changes.append('⚠️  A04: Botón hamburguesa no encontrado')

# ============================================================
# 15. SYNC aria-expanded in JS (A04)
# ============================================================
old_toggle_js = (
    "        menuToggle.addEventListener('click', () => {" + NL +
    "            navMenu.classList.toggle('active');" + NL +
    "        });"
)
new_toggle_js = (
    "        menuToggle.addEventListener('click', () => {" + NL +
    "            const isActive = navMenu.classList.toggle('active');" + NL +
    "            menuToggle.setAttribute('aria-expanded', isActive ? 'true' : 'false');" + NL +
    "            menuToggle.setAttribute('aria-label', isActive ? 'Cerrar menú de navegación' : 'Abrir menú de navegación');" + NL +
    "        });"
)
if old_toggle_js in content:
    content = content.replace(old_toggle_js, new_toggle_js, 1)
    changes.append('✅ A04: aria-expanded sincronizado en JS')
else:
    # Try alternate
    changes.append('⚠️  A04: JS toggle no encontrado — verificar manualmente')

# ============================================================
# 16. RESPECT prefers-reduced-motion in autoplay (C07)
# ============================================================
old_autoplay_start = "            // Arranque inicial" + NL + "            updateLayout(false);" + NL + "            startAutoplay();"
new_autoplay_start = (
    "            // Arranque inicial" + NL +
    "            updateLayout(false);" + NL +
    "            // Respetar preferencia de movimiento reducido (WCAG 2.3.3)" + NL +
    "            if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {" + NL +
    "                startAutoplay();" + NL +
    "            }"
)
if old_autoplay_start in content:
    content = content.replace(old_autoplay_start, new_autoplay_start)
    changes.append('✅ C07: Autoplay respeta prefers-reduced-motion')
else:
    changes.append('⚠️  C07: Bloque de autoplay no encontrado')

# ============================================================
# WRITE OUTPUT
# ============================================================
with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print(f'\nOriginal: {original_len} chars -> New: {len(content)} chars')
print(f'\nChanges applied ({len(changes)}):')
for c in changes:
    print(' ', c.encode('ascii', 'replace').decode())
