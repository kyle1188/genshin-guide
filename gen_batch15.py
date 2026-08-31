#!/usr/bin/env python3
# batch 15: combat-mechanics-guide + nahida-build
import sys, os, re
from pathlib import Path

ROOT = Path('E:/workbuddy/2026-07-29-09-05-15/genshin-guide')
GUIDES = ROOT / 'guides'
BASE = 'https://genshin-guide-one-five.vercel.app'
DATE = '2026-08-30'

sys.path.insert(0, 'E:/workbuddy/temp')
import importlib.util
spec = importlib.util.spec_from_file_location('gen', 'E:/workbuddy/temp/gen_articles.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    table_rows = []
    for line in lines:
        if line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(line.strip())
            continue
        else:
            if in_table and table_rows:
                html_lines.append('<table class="t">')
                for row in table_rows:
                    cells = [c.strip() for c in row.split('|')[1:-1]]
                    tag = 'th' if any(c.startswith('**') or c.startswith('<b>') for c in cells) else 'td'
                    html_lines.append('  <tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
                html_lines.append('</table>')
                in_table = False
                table_rows = []
        if line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:]}</h4>')
        elif '**' in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            html_lines.append(f'<p>{line}</p>')
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            html_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip() == '':
            pass
        else:
            html_lines.append(f'<p>{line}</p>')
    if in_table and table_rows:
        html_lines.append('<table class="t">')
        for row in table_rows:
            cells = [c.strip() for c in row.split('|')[1:-1]]
            html_lines.append('  <tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        html_lines.append('</table>')
    result = []
    in_li = False
    for line in html_lines:
        if line.startswith('<li>'):
            if not in_li:
                result.append('<ul>')
                in_li = True
            result.append(line)
        else:
            if in_li:
                result.append('</ul>')
                in_li = False
            result.append(line)
    if in_li:
        result.append('</ul>')
    return '\n'.join(result)

# Build entries as dicts (no triple-quoted strings with embedded quotes)
entries_data = [
    {
        'slug': 'combat-mechanics-guide',
        'zh_title': '原神战斗机制详解：元素附着/反应乘区/后台挂元素全攻略',
        'zh_h1': '原神战斗机制完全指南：从元素附了解到伤害公式',
        'zh_summary': '原神战斗机制全解析：元素附着频率、反应乘区原理、后台vs站场、元素抗性计算，帮你理解伤害是怎么算出来的。',
        'zh_desc': '原神战斗机制详解：元素附着频率/反应乘区/后台挂元素/元素抗性计算，理解伤害公式底层逻辑。',
        'zh_kw': 'genshin impact combat mechanics,genshin elemental reaction formula,原神战斗机制,元素附着频率,genshin damage formula',
        'zh_crumb': '攻略 › 战斗机制',
        'zh_lead': '原神伤害计算涉及多个乘区：基础伤害、增伤、暴击、防御、抗性、反应倍率。理解这些机制能帮你做出正确的配队和圣遗物选择，避免"堆歪"陷阱。',
        'zh_body_md': "## 战斗基础机制\n\n原神战斗的核心是元素反应系统。理解以下机制，能大幅提升你的输出效率。\n\n## 元素附着与频率\n\n元素附着（Elemental Application）是反应发生的前提。不同角色挂元素的频率差异巨大：\n\n| 角色 | 元素类型 | 挂元素频率 | 持续时间 |\n|------|----------|-----------|----------|\n| 行秋 | 水 | 高频（每 2s 一次） | 8s |\n| 班尼特 | 火 | 中频（每 3s 一次） | 6s |\n| 菲谢尔 | 雷 | 中频（每 4s 一次） | 10s |\n| 香菱 | 火 | 低频（每 6s 一次） | 12s |\n| 久岐忍 | 雷 | 持续接触 | 8s |\n| 纳西妲 | 草 | 中频（每 2.5s） | 6s |\n\n**关键原则**：高频挂元素的角色（行秋、菲谢尔）更适合当副 C，低频挂元素的角色（香菱）需要更长的输出窗口。\n\n## 元素反应乘区\n\n原神伤害公式中的"乘区"决定了反应队的伤害上限：\n\n```\n总伤害 = 基础伤害 × (1 + 增伤 %) × 暴击 × 防御 ↓ × 抗性 ↓ × 反应倍率\n```\n\n| 乘区 | 说明 | 示例 |\n|------|------|------|\n| 基础伤害 | 角色等级 + 武器 + 圣遗物 | 胡桃普攻 200% |\n| 增伤 % | 角色技能/武器/圣遗物 | 班尼特 +40% ATK |\n| 暴击 | 暴击率 × 暴击伤害 | 70/140 = CV 105 |\n| 防御 ↓ | 目标防御力 | 90 级怪 = 0.5 乘区 |\n| 抗性 ↓ | 元素抗性 | 100% 抗 = 减 90% 伤害 |\n| 反应倍率 | 蒸发 2x/融化 1.5x | 副 C 触发 = 2x |\n\n## 双附身机制（Dual Application）\n\n同一目标同时存在两种元素时，优先触发反应。常见的"双挂"策略：\n\n| 策略 | 用法 | 效果 |\n|------|------|------|\n| 水 + 火 | 行秋 E + 班尼特 Q | 蒸发队核心 |\n| 雷 + 草 | 菲谢尔 E + 纳西妲 E | 超绽放/激化 |\n| 冰 + 水 | 神里绫华 E + 行秋 E | 冻结控场 |\n| 火 + 雷 | 班尼特 Q + 菲谢尔 E | 超载 AOE |\n\n## 后台 vs 站场\n\n| 定位 | 特点 | 代表角色 |\n|------|------|----------|\n| 站场主 C | 长时间在场输出 | 胡桃、芙宁娜 |\n| 速切副 C | 短时间入场打爆发 | 夜兰、雷电将军 |\n| 后台辅助 | 全程后台挂元素/增伤 | 行秋、班尼特、万叶 |\n| 生存位 | 护盾/治疗 | 钟离、心海 |\n\n**运营原则**：后台角色先开 Q → 速切副 C 进场打爆发 → 站场主 C 站场输出 → 循环。\n\n## 元素抗性计算\n\n目标元素抗性影响最终伤害：\n\n| 抗性值 | 实际减伤 | 说明 |\n|--------|---------|------|\n| -80% | 减 44% 伤害 | 最低只能到 -80% |\n| 0% | 无减伤 | 标准状态 |\n| 10% | 减 9% 伤害 | 常见元素附着 |\n| 20% | 减 17% 伤害 | 部分 Boss 弱点 |\n| 50% | 减 33% 伤害 | 多数 Boss |\n| 100% | 减 90% 伤害 | 极高抗性 |\n\n> 抗性不能通过 Buff 降到 -80% 以下。钟离被动 + 万叶扩散 + 夜兰 E 可叠加至约 -40%。\n\n## FAQ\n\n**Q：为什么我的反应伤害很低？**\nA：检查是否满足三个条件：1）反应触发者等级够高；2）精通足够；3）目标没有被其他元素覆盖。\n\n**Q：后台角色和站场角色怎么选？**\nA：后台角色挂元素频率高、CD 短；站场角色输出窗口长。通常主 C 站场，辅助后台。\n\n**Q：元素附着可以被覆盖吗？**\nA：可以。新元素附着会清除旧元素，但有一定 overlap 时间。合理切换元素能最大化反应次数。\n\n**Q：反应乘区为什么重要？**\nA：乘区之间是乘法关系，比加法叠加收益更高。堆叠不同乘区（增伤 + 暴击 + 反应）比单一堆叠更优。",
        'zh_faq': [
            ('为什么我的反应伤害很低？', '检查：1）触发者等级够不够；2）精通够不够；3）目标元素是否被覆盖。'),
            ('后台角色和站场角色怎么选？', '后台角色挂元素频率高、CD短；站场角色输出窗口长。通常主C站场，辅助后台。'),
            ('元素附着可以被覆盖吗？', '可以。新元素附着会清除旧元素，但有短暂 overlap。合理切换元素能最大化反应次数。'),
            ('反应乘区为什么重要？', '乘区之间是乘法关系，比加法叠加收益更高。堆叠不同乘区（增伤+暴击+反应）比单一堆叠更优。'),
        ],
        'zh_pairbox': [
            ('/guides/elemental-reactions.html', '元素反应机制'),
            ('/guides/damage-formula-guide.html', '伤害公式'),
            ('/guides/team-building-guide.html', '配队原理'),
            ('/guides/elemental-mastery-guide.html', '元素精通'),
        ],
        'en_title': 'Genshin Impact Combat Mechanics: Applications, Multipliers & Reactions',
        'en_h1': 'Complete Combat Mechanics Guide: From Elemental Application to Damage Formula',
        'en_summary': 'Genshin Impact combat mechanics explained: elemental application frequency, reaction multiplier zones, off-field vs on-field, elemental resistance calculation.',
        'en_desc': 'Genshin Impact combat mechanics deep dive: application frequency, damage multiplier zones, off-field/on-field roles, resistance calculation.',
        'en_kw': 'genshin impact combat mechanics,genshin damage formula explained,elemental application guide,genshin reaction multipliers',
        'en_crumb': 'Guides › Combat Mechanics',
        'en_lead': 'Genshin damage calculation involves multiple multiplier zones: base DMG, DMG Bonus, CRIT, DEF, RES, and Reaction Multiplier. Understanding these mechanics helps you build smarter teams and avoid common stat-wasting mistakes.',
        'en_body_md': "## Core Combat Mechanics\n\nGenshin Impact's combat revolves around elemental reactions. Understanding these mechanics dramatically improves your damage output.\n\n## Elemental Application Frequency\n\nElemental Application is the prerequisite for reactions. Different characters apply elements at different frequencies:\n\n| Character | Element | Application Rate | Duration |\n|-----------|---------|-----------------|----------|\n| Xingqiu | Hydro | High (every 2s) | 8s |\n| Bennett | Pyro | Medium (every 3s) | 6s |\n| Fischl | Electro | Medium (every 4s) | 10s |\n| Xiangling | Pyro | Low (every 6s) | 12s |\n| Kuki Shinobu | Electro | Continuous contact | 8s |\n| Nahida | Dendro | Medium (every 2.5s) | 6s |\n\n**Key principle**: High-frequency applicators (Xingqiu, Fischl) work best as sub-DPS. Low-frequency applicators (Xiangling) need longer DPS windows.\n\n## Reaction Multipliers (乘区)\n\nThe damage formula's \"multiplier zones\" determine reaction team ceilings:\n\n```\nTotal DMG = Base DMG x (1 + DMG Bonus %) x CRIT x DEF ↓ x RES ↓ x Reaction Multiplier\n```\n\n| Multiplier | Description | Example |\n|------------|-------------|---------|\n| Base DMG | Character lvl + Weapon + Artifacts | Hu Tao normal attack 200% |\n| DMG Bonus % | Skill/Weapon/Artifact | Bennett +40% ATK |\n| CRIT | CRIT Rate x CRIT DMG | 70/140 = CV 105 |\n| DEF ↓ | Target DEF | AR 90 = 0.5 multiplier |\n| RES ↓ | Elemental RES | 100% RES = -90% DMG |\n| Reaction Mult | Vaporize 2x/Melt 1.5x | Sub-DPS triggers = 2x |\n\n## Dual Application Strategy\n\nWhen two elements coexist on a target, reactions trigger first. Common pairing strategies:\n\n| Strategy | Usage | Effect |\n|----------|-------|--------|\n| Hydro + Pyro | Xingqiu E + Bennett Q | Vaporize core |\n| Electro + Dendro | Fischl E + Nahida E | Hyperbloom/Burn |\n| Cryo + Hydro | Ayaka E + Xingqiu E | Freeze control |\n| Pyro + Electro | Bennett Q + Fischl E | Overload AoE |\n\n## On-Field vs Off-Field\n\n| Role | Characteristics | Examples |\n|------|----------------|----------|\n| On-Field Main DPS | Long uptime, consistent output | Hu Tao, Furina |\n| Quick-Switch Sub DPS | Short burst windows | Yelan, Raiden |\n| Off-Field Support | Passive element application/buffs | Xingqiu, Bennett, Kazuha |\n| Shielder/Healer | Survival utility | Zhongli, Kokomi |\n\n**Rotation principle**: Off-field skills first -> Sub DPS burst -> Main DPS on-field -> Loop.\n\n## Elemental Resistance Calculation\n\nTarget resistance directly impacts final damage:\n\n| RES Value | Damage Reduction | Notes |\n|-----------|-----------------|-------|\n| -80% | -44% DMG taken | Floor is -80% |\n| 0% | None | Standard |\n| 10% | -9% DMG | Common application |\n| 20% | -17% DMG | Some boss weaknesses |\n| 50% | -33% DMG | Most bosses |\n| 100% | -90% DMG | Extreme resistance |\n\n> Max shred is -80%. Zhongli passive + Kazuha Swirl + Yelan E can stack to approximately -40%.\n\n## FAQ\n\n**Q: Why are my reaction damages so low?**\nA: Check three conditions: 1) Is the reaction triggerer's level high enough? 2) Is EM sufficient? 3) Is the target's existing element still active?\n\n**Q: How do I choose between on-field and off-field roles?**\nA: Off-field characters have high application frequency and short CDs. On-field characters have longer DPS windows. Usually: main DPS on-field, supports off-field.\n\n**Q: Can elemental applications overwrite each other?**\nA: Yes. New applications clear old ones after a brief overlap window. Strategic element switching maximizes reaction count.\n\n**Q: Why do multiplier zones matter?**\nA: Multipliers are multiplicative, not additive. Stacking different multiplier types (DMG Bonus + CRIT + Reactions) outperforms single-stacking.",
        'en_faq': [
            ("Why are my reaction damages so low?", "Check: 1) Is the triggerer level high enough? 2) Is EM sufficient? 3) Is the target's existing element still active?"),
            ('How do I choose between on-field and off-field roles?', 'Off-field = high freq application, short CD. On-field = long DPS windows. Usually: main DPS on-field, supports off-field.'),
            ('Can elemental applications overwrite each other?', 'Yes. New applications clear old ones after a brief overlap window. Strategic switching maximizes reaction count.'),
            ('Why do multiplier zones matter?', 'Multipliers are multiplicative, not additive. Stacking different multiplier types (DMG Bonus + CRIT + Reactions) outperforms single-stacking.'),
        ],
        'en_pairbox': [
            ('/guides/elemental-reactions-en.html', 'Elemental Reactions'),
            ('/guides/damage-formula-guide-en.html', 'Damage Formula'),
            ('/guides/team-building-guide-en.html', 'Team Building'),
            ('/guides/elemental-mastery-guide-en.html', 'Elemental Mastery'),
        ],
    },
    {
        'slug': 'nahida-build',
        'zh_title': '纳西妲配装指南：圣遗物/武器/天赋/配队 2026',
        'zh_h1': '纳西妲完全配装指南：从入门到毕业',
        'zh_summary': '原神纳西妲配装全攻略：圣遗物推荐（饰金/深林）、武器选择、天赋升级优先级、超绽放/激化/燃烧队配队方案。',
        'zh_desc': '纳西妲配装完全指南：圣遗物/武器/天赋/配队全解析，从零氪到满精炼毕业方案。',
        'zh_kw': 'genshin nahida build guide,nahida artifacts,nahida team comp,genshin dandalo build,纳西妲配装',
        'zh_crumb': '攻略 › 纳西妲配装',
        'zh_lead': '纳西妲是原神最强的草系辅助，超绽放/激化/燃烧队的核心。本文详解她的圣遗物、武器、天赋升级和配队方案，帮你把她用到极致。',
        'zh_body_md': "## 纳西妲配装完全指南\n\n纳西妲是原神中最强草系辅助，也是草体系（超绽放/激化/燃烧）的核心发动机。她的元素战技「妙识天圆」能提供全队草附着，元素爆发「菩提眷念」能引爆敌人身上的所有草元素。\n\n## 定位\n\n| 定位 | 说明 |\n|------|------|\n| 草元素挂附 | 战场挂草频率最高，每 2.5s 一次 |\n| 激化/超绽放触发 | 草系 2nd-applier，触发反应伤害 |\n| 全队增伤 | E 技能长按提供全队草元素伤害加成 |\n| 精通转伤 | 天赋「慧心」将精通转化为队伍总伤害 |\n\n## 圣遗物推荐\n\n| 套装 | 2 件效果 | 4 件效果 | 适用场景 |\n|------|---------|---------|----------|\n| 饰金之梦 | 精通 +80 | 草伤/精通 +20% | 超绽放队首选 |\n| 深林的记忆 | 草伤 +15% | 敌方草抗 -30% | 激化队首选 |\n| 千岩牢固 | 生命 +20% | 护盾强效 +20% | 生存向 |\n\n**圣遗物主词条优先级**：\n- 沙漏：元素精通 > 充能效率 > 攻击力\n- 杯槽：草元素伤害加成 > 元素精通\n- 头冠：元素精通 > 暴击率 > 暴击伤害\n\n**圣遗物副词条优先级**：元素精通 > 充能效率 > 暴击率 > 暴击伤害\n\n## 武器推荐\n\n| 武器 | 精炼 | 适配度 | 说明 |\n|------|------|--------|------|\n| 若水 | R1 | ⭐⭐⭐⭐⭐ | 最佳专武，精通转伤害 |\n| 西福斯的月光 | R1 | ⭐⭐⭐⭐ | 四星祭品，精通 + 充能 |\n| 铁影.keyboard | R1 | ⭐⭐⭐ | 锻造武器，纯精通 |\n| 流浪乐章 | R1 | ⭐⭐⭐ | 赌命武器，爆发时极强 |\n| 王下近侍 | R1 | ⭐⭐ | 泛用辅助，增伤为主 |\n\n## 天赋升级优先级\n\n| 天赋 | 升级理由 | 优先级 |\n|------|---------|--------|\n| 元素战技「妙识天圆」 | 挂草频率核心，升级提升草丛持续时间 | S+ |\n| 元素爆发「菩提眷念」 | 引爆草丛，升级提升伤害 | S |\n| 普通攻击 | 几乎不普攻，不升级 | D |\n\n**建议等级**：E 10 级 / Q 8 级 / A 1 级\n\n## 配队推荐\n\n### 超绽放队（F2P 最强体系）\n\n| 位置 | 角色 | 理由 |\n|------|------|------|\n| 草辅/触发 | 纳西妲 | 挂草 + 激化触发 |\n| 超绽放触发 | 久岐忍 | 绝缘套 + 180% 充能 |\n| 挂水系 | 行秋/夜兰 | 高频挂水 |\n| 护盾 | 钟离 | 无敌护盾 |\n\n### 激化队\n\n| 位置 | 角色 | 理由 |\n|------|------|------|\n| 草辅 | 纳西妲 | 挂草 |\n| 雷 C | 提纳里/雷泽 | 激化主 C |\n| 增伤 | 班尼特 | ATK + 治疗 |\n| 生存 | 钟离/迪奥娜 | 护盾/治疗 |\n\n### 燃烧队\n\n| 位置 | 角色 | 理由 |\n|------|------|------|\n| 草辅 | 纳西妲 | 挂草触发燃烧 |\n| 火 C | 玛薇卡 | 燃烧主 C |\n| 风辅 | 万叶 | 扩散增伤 |\n| 生存 | 钟离 | 护盾 |\n\n## FAQ\n\n**Q：纳西妲必须堆精通吗？**\nA：是的。纳西妲的天赋「慧心」将精通转化为全队伤害加成，精通越高全队越强。\n\n**Q：纳西妲带绝缘套还是饰金？**\nA：超绽放队首选饰金（精通转伤害）；激化队可选深林（草伤 + 减抗）。\n\n**Q：纳西妲的 E 技能长按和短按有什么区别？**\nA：短按产生 3 个法奇菈（每个挂草 2s）；长按产生 5 个法奇菈，并提供全队草伤加成（20s）。\n\n**Q：纳西妲适合零氪玩家吗？**\nA：非常合适。纳西妲是零氪玩家最值得投入的草系角色，配合久岐忍可构成最强的 F2P 反应体系。",
        'zh_faq': [
            ('纳西妲必须堆精通吗？', '是的。纳西妲的天赋「慧心」将精通转化为全队伤害加成，精通越高全队越强。'),
            ('纳西妲带绝缘套还是饰金？', '超绽放队首选饰金（精通转伤害）；激化队可选深林（草伤 + 减抗）。'),
            ('纳西妲的 E 技能长按和短按有什么区别？', '短按产生 3 个法奇菈（每个挂草 2s）；长按产生 5 个法奇菈，并提供全队草伤加成（20s）。'),
            ('纳西妲适合零氪玩家吗？', '非常合适。纳西妲是零氪玩家最值得投入的草系角色，配合久岐忍可构成最强的 F2P 反应体系。'),
        ],
        'zh_pairbox': [
            ('/guides/character-tier-list.html', '角色强度排行'),
            ('/guides/elemental-reaction-teams.html', '元素反应配队'),
            ('/guides/artifact-sets-guide.html', '圣遗物套装'),
            ('/guides/elemental-mastery-guide.html', '元素精通'),
        ],
        'en_title': 'Nahida Build Guide 2026: Artifacts, Weapons, Talents & Teams',
        'en_h1': 'Complete Nahida Build Guide: From Beginner to Endgame',
        'en_summary': 'Genshin Impact Nahida build guide: artifact sets (Golden Troupe/Deepwood), weapon recommendations, talent priorities, Hyperbloom/Aggravate/Burning team comps.',
        'en_desc': 'Nahida complete build guide: artifacts, weapons, talents, teams — from F2P to R5 endgame.',
        'en_kw': 'genshin nahida build guide,nahida artifacts,genshin dandalo build,nahida team comp,nahida guide',
        'en_crumb': 'Guides › Nahida Build',
        'en_lead': 'Nahida is the strongest Dendro support in Genshin Impact and the core of all Dendro teams. This guide covers her artifacts, weapons, talent priorities, and team compositions to help you maximize her potential.',
        'en_body_md': "## Complete Nahida Build Guide\n\nNahida is the strongest Dendro support in Genshin Impact and the core engine of all Dendro teams (Hyperbloom, Aggravate, Spread, Burning). Her Elemental Skill「妙识天圆」applies Dendro at the highest frequency, while her Burst「菩提眷念」ignites all Dendro on enemies.\n\n## Role Overview\n\n| Role | Description |\n|------|-------------|\n| Dendro Application | Highest field Dendro application rate, every 2.5s |\n| Aggravate/Hyperbloom Trigger | Dendro 2nd-applier, triggers reaction DMG |\n| Team DMG Boost | Hold E for team-wide Dendro DMG bonus |\n| EM-to-DMG Conversion | Talent「慧心」converts EM to team total DMG |\n\n## Artifact Recommendations\n\n| Set | 2-Pc Bonus | 4-Pc Bonus | Best For |\n|-----|-----------|------------|----------|\n| Golden Troupe | EM +80 | Dendro DMG/EM +20% | Hyperbloom (primary) |\n| Deepwood Memories | Dendro DMG +15% | Enemy RES -30% | Aggravate (primary) |\n| Verdant Legend | HP +20% | Shield strength +20% | Survivability |\n\n**Main stat priority**:\n- Sands: EM > ER > ATK\n- Goblet: Dendro DMG Bonus > EM\n- Circlet: EM > CRIT Rate > CRIT DMG\n\n**Substat priority**: EM > ER > CRIT Rate > CRIT DMG\n\n## Weapon Recommendations\n\n| Weapon | Refinement | Suitability | Notes |\n|--------|-----------|-------------|-------|\n| Aqua Simulacra | R1 | ⭐⭐⭐⭐⭐ | Best-in-slot, EM-to-DMG |\n| Favonius Codex | R1 | ⭐⭐⭐⭐ | 4-star祭品, EM + ER |\n| Iron Sting | R1 | ⭐⭐⭐ | Forged, pure EM |\n| Summer Time Recall | R1 | ⭐⭐⭐ | RNG weapon, insane bursts |\n| Key of Khaj-Nisut | R1 | ⭐⭐ | Universal support, shred-focused |\n\n## Talent Priority\n\n| Talent | Reason | Priority |\n|--------|--------|----------|\n| Elemental Skill「妙识天圆」 | Core Dendro application, longer duration | S+ |\n| Elemental Burst「菩提眷念」 | Dendro explosion, scales with level | S |\n| Normal Attack | Rarely used | D |\n\n**Recommended levels**: E 10 / Q 8 / A 1\n\n## Team Compositions\n\n### Hyperbloom Team (Best F2P Archetype)\n\n| Slot | Character | Reason |\n|------|-----------|--------|\n| Dendro Applyer | Nahida | Field Dendro application |\n| Hyperbloom Trigger | Kuki Shinobu | Emblem + 180% ER |\n| Hydro Applyer | Xingqiu/Yelan | High-freq Hydro |\n| Shield | Zhongli | Indestructible shield |\n\n### Aggravate Team\n\n| Slot | Character | Reason |\n|------|-----------|--------|\n| Dendro Applyer | Nahida | Dendro application |\n| Electro DPS | Tighnari/Razor | Aggravate main DPS |\n| Buffer | Bennett | ATK buff + healing |\n| Shield | Zhongli/Diona | Protection |\n\n### Burning Team\n\n| Slot | Character | Reason |\n|------|-----------|--------|\n| Dendro Applyer | Nahida | Triggers Burning |\n| Pyro DPS | Mavuika | Burning main DPS |\n| Anemo Support | Kazuha | Swirl + shred |\n| Shield | Zhongli | Protection |\n\n## FAQ\n\n**Q: Does Nahida need to stack EM?**\nA: Yes. Nahida's talent「慧心」converts EM into team-wide DMG bonus — more EM = stronger team.\n\n**Q: Nahida: Golden Troupe or Deepwood?**\nA: Hyperbloom → Golden Troupe (EM conversion). Aggravate → Deepwood (Dendro DMG + RES shred).\n\n**Q: What's the difference between short and long press E?**\nA: Short press spawns 3 Paimon friends (each applies Dendro for 2s). Hold E spawns 5 and grants team-wide Dendro DMG bonus for 20s.\n\n**Q: Is Nahida worth pulling for F2P?**\nA: Absolutely. She's the most valuable Dendro character for F2P players. Paired with Kuki Shinobu, she forms the strongest F2P reaction team in the game.",
        'en_faq': [
            ('Does Nahida need to stack EM?', "Yes. Nahida's talent converts EM into team-wide DMG bonus — more EM = stronger team."),
            ('Nahida: Golden Troupe or Deepwood?', 'Hyperbloom -> Golden Troupe (EM conversion). Aggravate -> Deepwood (Dendro DMG + RES shred).'),
            ("What's the difference between short and long press E?", 'Short press spawns 3 Paimon friends (each applies Dendro for 2s). Hold E spawns 5 and grants team-wide Dendro DMG bonus for 20s.'),
            ('Is Nahida worth pulling for F2P?', "Absolutely. She's the most valuable Dendro character for F2P players. Paired with Kuki Shinobu, she forms the strongest F2P reaction team."),
        ],
        'en_pairbox': [
            ('/guides/character-tier-list-en.html', 'Character Tier List'),
            ('/guides/elemental-reaction-teams-en.html', 'Elemental Reaction Teams'),
            ('/guides/artifact-sets-guide-en.html', 'Artifact Sets'),
            ('/guides/elemental-mastery-guide-en.html', 'Elemental Mastery'),
        ],
    },
]

# Generate HTML files
for entry in entries_data:
    slug = entry['slug']
    
    # Build zh entry
    zh_d = {
        'title': entry['zh_title'],
        'h1': entry['zh_h1'],
        'summary': entry['zh_summary'],
        'desc': entry['zh_desc'],
        'kw': entry['zh_kw'],
        'crumb': entry['zh_crumb'],
        'lead': entry['zh_lead'],
        'body': md_to_html(entry['zh_body_md']),
        'faq': entry['zh_faq'],
        'pairbox': entry['zh_pairbox'],
    }
    
    # Build en entry
    en_d = {
        'title': entry['en_title'],
        'h1': entry['en_h1'],
        'summary': entry['en_summary'],
        'desc': entry['en_desc'],
        'kw': entry['en_kw'],
        'crumb': entry['en_crumb'],
        'lead': entry['en_lead'],
        'body': md_to_html(entry['en_body_md']),
        'faq': entry['en_faq'],
        'pairbox': entry['en_pairbox'],
    }
    
    for lang, d in [('zh', zh_d), ('en', en_d)]:
        fn = GUIDES / f'{slug}.html' if lang == 'zh' else GUIDES / f'{slug}-en.html'
        zh_u = f'{BASE}/guides/{slug}.html'
        en_u = f'{BASE}/guides/{slug}-en.html'
        self_u = zh_u if lang == 'zh' else en_u
        other = en_u if lang == 'zh' else zh_u
        lang_txt = 'EN' if lang == 'zh' else '中文'
        back = '← 返回首页' if lang == 'zh' else '← Back to Home'
        site = '提瓦特开荒攻略站' if lang == 'zh' else 'Teyvat Starter Guide'

        head = G.head(lang, slug, d['title'], d['desc'], d['kw'])
        jsonld = G.article_jsonld(d['title'], d['desc'], self_u, lang) + G.faq_jsonld(d['faq'])
        topbar = G.topbar(lang, other, back, lang_txt, other)
        faq_title = '快速问答' if lang == 'zh' else 'Quick Answers'
        faq_html = f'<section class="faq"><h2>{faq_title}</h2>'
        for q, a in d['faq']:
            faq_html += f'<div class="qa"><h3>{q}</h3><p>{a}</p></div>'
        faq_html += '</section><div class="pairbox">'
        for u, t in d['pairbox']:
            faq_html += f'<a href="{u}">{t}</a>'
        faq_html += '</div>'
        body = (f'<div class="wrap"><nav class="crumb"><a href="/">{site}</a> › {d["crumb"]}</nav><article>'
                f'<h1>{d["h1"]}</h1><p class="lead">{d["lead"]}</p>{d["body"]}{faq_html}</article></div>')
        html = head + jsonld + topbar + body + G.tail(lang)

        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'wrote {fn}')

# Update sitemap
sm = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
new_blocks = ''
for entry in entries_data:
    slug = entry['slug']
    zh_u = f'{BASE}/guides/{slug}.html'
    en_u = f'{BASE}/guides/{slug}-en.html'
    if zh_u not in sm:
        new_blocks += G.sitemap_block(zh_u, en_u)
if new_blocks:
    marker = '<!-- LONGTAIL -->'
    if marker in sm:
        sm = sm.replace(marker, new_blocks + marker, 1)
    else:
        sm = sm.replace('</urlset>', new_blocks + '</urlset>', 1)
    (ROOT / 'sitemap.xml').write_text(sm, encoding='utf-8')
    print('sitemap updated')
else:
    print('sitemap already up to date')
print('DONE')
