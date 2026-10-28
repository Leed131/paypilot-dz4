# Multi-turn Test Plan + Degradation Profile — PayPilot

## 1. Контекст і прогноз

**Питання CTO:** як правильні поодинокі факти можуть дати неправильний результат справи?
Відповідь за нашими прогонами: після згортки агент утрачає точні параметри і підміняє reason code;
потім відновлює суму й дату з транзакцій, а підміну коду не виправляє. Однакове вікно двох кодів
залишає дедлайн правильним і маскує помилку. У старій лабораторній це дійшло до створення спору
з неправильним кодом у 4/5 діалогів. Нові діагностичні кейси явно просять не відкривати спір.

| Параметр | Значення |
|---|---|
| Система | PayPilot; лише навчальні дані Verta |
| Профілі | clean: без активних дефектів; lesson-05: D06,D07 |
| Модель / провайдер | gpt-5-mini-2025-08-07 / OpenAI, підтверджено usage і llm.call у трейсі |
| Сценарій | C-07; клієнт CUS-0004, TX-0401, 240.00 EUR |
| Дата транзакції / тестового рушія | 2026-07-20 / 2026-09-15 |
| Правильний код / вікно / дедлайн | goods_not_received / 90 днів / 2026-10-18; підтверджено власним check_dispute_eligibility |
| Набір | l05_dialogs.jsonl; 5 кейсів memory; runs:5; gate:release; set_hash `67ca1d4fe79f` |
| Дата запусків | 28 жовтня 2026; сирі часові позначки звітів — UTC |
| clean | 5/5 кейсів, 25/25 діалогів; reports/l05_dialogs-clean-20261028T195254.json |
| lesson-05 | 1/5 кейсів, 8/25 діалогів; reports/l05_dialogs-lesson-05-20261028T204910.json |

**Прогноз нового набору** закомічено окремо: [6d73873](https://github.com/Leed131/paypilot-dz4/commit/6d73873034cfbb83e1c4dd94f9e445ceab540503) — вивід git log надано до запусків.
Через GitHub перевірено: коміт є предком main, дата коміту 19:49:34 UTC, початок clean 19:52:54 UTC.
Це перевірка часу коміту та вмісту; перше завантаження на GitHub відбулося після прогонів.
Незмінний початковий README збережено в evidence/forecast-before-runs.md; його Git blob — `ce58b35c5f08a31114d0583b0d4bccf1ce9adcc3`.
Прогноз спирався на вже проведену лабораторну, тому не є сліпим. Очікували PASS усіх кейсів на clean;
на lesson-05 — FAIL H01,H02,H03,H05, PASS H04. Крок втрати — 3; прояв H01/H03/H05 — 5, H02 — 4.
На рівні кейсів прогноз збігся. H05 порушив інваріант лише у 2/5 повторів; причину трьох успіхів наведено нижче.
Лабораторний прогноз кроку 3 був записаний у чаті, а його локальний файл/коміт не надано; його не підмінюємо цим новим комітом.

**Відмінності від тексту заняття.** Фактичне вікно — 90, а не 120 днів. Використано CUS-0004 з ДЗ та раннера,
а не CUS-0009 зі старої версії шаблону. Поріг рахує кроки: після двох кроків згортка спрацьовує на третьому.
H01 — діагностичний варіант C-07 з тією самою справою й сімома кроками: питання про FX прямо просить тарифний відсоток,
а проби прямо просять параметри. Це прибрало неоднозначність старої FX-репліки; старі сирі результати 3/4 на clean збережено в reports/lab.
Попередні golden.jsonl та репозиторії ДЗ не змінювалися.

## 2. Профіль деградації

### 2.1. Контрольний H01 на clean, прогін 1

| Крок | Репліка клієнта | Репліка агента — витяг | Відомі вхідні дані / історія | Пошук у документації |
|---|---|---|---|---|
| 1 | I'm CUS-0004. Transaction TX-0401, 240.00 EUR: the goods never arrived. Which reason code applies? State the transaction ID and amount too. Do not open a dispute. | What I did<br>- Retrieved your account record to confirm I’m acting for CUS-0004.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Applicable dispute reason code: goods_not_received<br><br>What happens next<br>- I will not open a dispute (per your instruction). If you want me to open one later, I must first run an eligibility check (check_dispute_eligibility) and — if eligible — I can create the dispute on your behalf. If you’d like guidance on what evidence to gather (order confirmation, tracking, seller corresp… | Поточна репліка: TX-0401, 240.00 EUR, опис недоставки. Попередньої історії немає. | search_knowledge_base не викликано; само по собі це не дефект. |
| 2 | Can I dispute it? Use the official eligibility tool for that transaction and reason. State the transaction date, filing window in days, deadline, reason code and amount. Do not open a dispute. | What I did<br>- Ran the official eligibility check (check_dispute_eligibility) for transaction TX-0401 with reason code goods_not_received.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Transaction date: 2026-07-20<br>- Filing window: 90 days<br>- Deadline to file: 2026-10-18 (eligibility checked as of 2026-09-15)<br>- Reason code: goods_not_received<br>- Eligibility result: eligible = true<br><br>What happens next<br>- I will not open a dispute (per your instruction). If you want me to proceed before the deadline, tell m… | Крок 1: TX-0401, 240.00 EUR, goods_not_received. Рушій цього кроку повертає 90 днів, 2026-07-20 і 2026-10-18, as_of 2026-09-15. | search_knowledge_base не викликано; само по собі це не дефект. |
| 3 | What is my daily outgoing transfer limit in EUR? | What I did<br>- Retrieved your account (ACC-1005) and checked your transfer limits.<br><br>What I found<br>- Daily outgoing transfer limit: €5,000 (as of 2026-09-15).<br>- Daily spent: €0 — Daily remaining: €5,000.<br><br>What happens next<br>- If you’d like to request a limit increase or need help with a transfer, tell me and I can escalate this to a human agent. | summary.text містить усі п’ять параметрів справи та дедлайн. | search_knowledge_base не викликано; само по собі це не дефект. |
| 4 | According to the tariff, what is the standard FX spread percentage for my tier? Give the percentage. | What I did<br>- Searched the tariff schedule in the knowledge base for FX spreads by tier.<br><br>What I found<br>- Standard FX spread for your tier (Tier 1): 1.5%.<br><br>What happens next<br>- If you want, I can run a live FX quote for a specific amount and currency pair showing mid rate, spread, allowance and the final converted amount. | Згортка з правильними параметрами + наступні репліки та tool results. Повний messages не журналюється. | `tariffs.md#s2`: Verta tariff schedule<br>## FX spreads by tier<br>The spread is applied over the mid-market rate only after the free monthly<br>conversion allowance is exhausted.<br><br>\| Tier \| FX spread \| Free monthly conversion allowance \|<br>\|---\|---\|---\|<br>\| Tier 1 \| 1.5% \| EUR 50…<br>`glossary.md#s2`: Glossary<br>## Spread<br>The percentage Verta adds to the mid-market rate on a conversion. The spread<br>depends on the customer tier.<br>`fx-guide.md#s2`: Currency conversion guide<br>## Reading a quote<br>A complete quote lists: mid rate, spread percentage applied, allowance total<br>and allowance used before this conversion, gross converted amount, spread<br>amount, and the final credited amount. The final amoun…<br>`fx-guide.md#s1`: Currency conversion guide<br>## How a conversion is priced<br>A conversion quote has these components, in order: the mid-market rate for the<br>currency pair; the tier spread (a percentage of the gross converted amount);<br>the free monthly conversion allowance.… |
| 5 | Fine. Back to that charge — what do I do next? First state its exact transaction ID, amount and reason code. Do not open a dispute. | What I did<br>- Reviewed your account and the previous eligibility check I ran for the charge.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: €240.00<br>- Reason code: goods_not_received<br>- Additional details from the earlier eligibility check (as_of 2026-09-15): transaction date 2026-07-20, filing window 90 days, deadline to file reported as 2026-10-18, and the check returned eligible.<br><br>What happens next (I will not open a dispute unless you ask)<br>- If you want to prepare now: I can list recommended evidence for a good… | Згортка з правильними параметрами + наступні репліки та tool results. Повний messages не журналюється. | search_knowledge_base не викликано; само по собі це не дефект. |
| 6 | 240 euro, as I said at the start. | What I did<br>- Rechecked the transaction record and the eligibility result we ran earlier.<br><br>What I found<br>- Transaction ID: TX-0401  <br>- Amount: €240.00 (confirmed)  <br>- Merchant: TechMart Online  <br>- Transaction date: 2026-07-20  <br>- Reason code: goods_not_received  <br>- Eligibility (as of 2026-09-15): eligible = true; filing window 90 days; deadline to file = 2026-10-18; status = settled.<br><br>What happens next (I will not open a dispute unless you ask)<br>- I can list recommended evidence to support a goods_not_received dispute… | Згортка з правильними параметрами + наступні репліки та tool results. Повний messages не журналюється. | search_knowledge_base не викликано; само по собі це не дефект. |
| 7 | And I still have time to file, right? State the original transaction's reason code, transaction date, filing window in days and filing deadline. Do not open a dispute. | What I did<br>- Re-ran the official eligibility check for TX-0401 with reason code goods_not_received.<br><br>What I found<br>- Reason code: goods_not_received<br>- Transaction date: 2026-07-20<br>- Filing window: 90 days<br>- Filing deadline: 2026-10-18<br>- Eligibility: eligible = true (as of 2026-09-15)<br><br>What happens next<br>- I will not open a dispute unless you explicitly ask. If you want, I can list the evidence you should gather or send an account statement to your registered email. | Згортка з правильними параметрами + наступні репліки та tool results. Повний messages не журналюється. | search_knowledge_base не викликано; само по собі це не дефект. |

На кроці 3 summary.text явно зберігає TX-0401, 240.00 EUR, goods_not_received, 2026-07-20 і 90 днів.
Доказ: traces/20261028T195254/CONV-H01-run1-turn3.json, request e8ef8a6dc88b4a62, span 71684251dd8248a5.
Параметри в перевірених відповідях тримаються до кроку 7 у всіх 5 повторах.

### 2.2. H01 на lesson-05, прогін 1

| Крок | Репліка клієнта | Репліка агента — витяг | Відомі вхідні дані / історія | Пошук у документації |
|---|---|---|---|---|
| 1 | I'm CUS-0004. Transaction TX-0401, 240.00 EUR: the goods never arrived. Which reason code applies? State the transaction ID and amount too. Do not open a dispute. | What I did<br>- Retrieved your account and recent transactions for ACC-1005.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Merchant: TechMart Online<br>- Date: 2026-07-20<br>- Status: settled<br><br>Applicable reason code<br>- goods_not_received<br><br>What happens next<br>- I did not open a dispute. If you’d like me to proceed, I will first check dispute eligibility for TX-0401 and then open the dispute if eligible. Would you like me to do that? | Поточна репліка: TX-0401, 240.00 EUR, опис недоставки. Попередньої історії немає. | search_knowledge_base не викликано; само по собі це не дефект. |
| 2 | Can I dispute it? Use the official eligibility tool for that transaction and reason. State the transaction date, filing window in days, deadline, reason code and amount. Do not open a dispute. | What I did<br>- Checked dispute eligibility for transaction TX-0401 using the official eligibility tool.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Transaction date: 2026-07-20<br>- Reason code checked: goods_not_received<br>- Filing window (days): 90<br>- Deadline to file: 2026-10-18<br>- Eligibility result: eligible = true<br><br>What happens next<br>- I did not open a dispute. If you want me to proceed, I can open the dispute for TX-0401 under goods_not_received (next step would be to create the dispute). Would you … | Крок 1: TX-0401, 240.00 EUR, goods_not_received. Рушій цього кроку повертає 90 днів, 2026-07-20 і 2026-10-18, as_of 2026-09-15. | search_knowledge_base не викликано; само по собі це не дефект. |
| 3 | What is my daily outgoing transfer limit in EUR? | What I did<br>- I checked your account and current transfer limits.<br><br>What I found<br>- Account: ACC-1005 (EUR), balance 1,310.20 EUR.<br>- Tier: tier1 (as of 2026-09-15).<br>- Daily outgoing transfer limit: 5,000 EUR.<br>- Daily remaining today: 5,000 EUR.<br><br>What happens next<br>- If you want to make a transfer, tell me the amount and which account to use and I’ll proceed.<br>- If you’d like to request a limit increase, I can escalate that to a human agent — tell me if you want me to do that. | summary.text без суми, ID і точних дат; goods_not_received замінено на service_not_rendered. | search_knowledge_base не викликано; само по собі це не дефект. |
| 4 | According to the tariff, what is the standard FX spread percentage for my tier? Give the percentage. | What I did<br>- I checked Verta’s tariff schedule for FX spreads.<br><br>What I found<br>- Your tier (tier1 / Tier 1) standard FX spread: 1.5%.<br><br>What happens next<br>- If you’d like, I can show the full tariff entry or run a live FX quote for a specific amount to show the rate, allowance usage and final amount. Which would you prefer? | Пошкоджена згортка + репліки про ліміт; початкові точні параметри з неї не повернулися. | `tariffs.md#s2`: Verta tariff schedule<br>## FX spreads by tier<br>The spread is applied over the mid-market rate only after the free monthly<br>conversion allowance is exhausted.<br><br>\| Tier \| FX spread \| Free monthly conversion allowance \|<br>\|---\|---\|---\|<br>\| Tier 1 \| 1.5% \| EUR 50…<br>`glossary.md#s2`: Glossary<br>## Spread<br>The percentage Verta adds to the mid-market rate on a conversion. The spread<br>depends on the customer tier.<br>`fx-guide.md#s2`: Currency conversion guide<br>## Reading a quote<br>A complete quote lists: mid rate, spread percentage applied, allowance total<br>and allowance used before this conversion, gross converted amount, spread<br>amount, and the final credited amount. The final amoun…<br>`fx-guide.md#s1`: Currency conversion guide<br>## How a conversion is priced<br>A conversion quote has these components, in order: the mid-market rate for the<br>currency pair; the tier spread (a percentage of the gross converted amount);<br>the free monthly conversion allowance.… |
| 5 | Fine. Back to that charge — what do I do next? First state its exact transaction ID, amount and reason code. Do not open a dispute. | What I did<br>- I reviewed your recent settled card transactions for ACC-1005.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Reason code to use: service_not_rendered<br><br>What happens next (I will not open a dispute now)<br>- First, try contacting the merchant with your order/booking reference and request a refund. Keep copies of any responses.<br>- Collect evidence to support a dispute if needed: order confirmation, delivery/tracking details, merchant messages, screenshots and the card receipt.<br>- When you’re r… | Пошкоджена згортка; get_transactions повертає TX-0401 і 240 EUR. Код лишається service_not_rendered. | search_knowledge_base не викликано; само по собі це не дефект. |
| 6 | 240 euro, as I said at the start. | What I did<br>- I reviewed the settled card transaction we discussed.<br><br>What I found<br>- Transaction ID: TX-0401<br>- Amount: 240.00 EUR<br>- Reason code to use: service_not_rendered<br>- (You previously confirmed I ran the eligibility check and the transaction is eligible to be disputed.)<br><br>What happens next<br>- I will not open a dispute unless you explicitly tell me to proceed.<br>- Next recommended steps: contact the merchant for a refund and keep any replies; gather evidence (order, tracking, messages, screenshots).<br>- When you’re r… | Клієнт повторює 240 EUR. У пізнішій історії вже є відновлені ID/сума і підмінений код. | search_knowledge_base не викликано; само по собі це не дефект. |
| 7 | And I still have time to file, right? State the original transaction's reason code, transaction date, filing window in days and filing deadline. Do not open a dispute. | What I did<br>- I ran the official eligibility check for the settled charge (TX-0401).<br><br>What I found<br>- Transaction ID: TX-0401<br>- Reason code: service_not_rendered<br>- Transaction date: 2026-07-20<br>- Filing window: 90 days<br>- Filing deadline: 2026-10-18<br>- Eligibility: eligible to be disputed<br><br>What happens next<br>- You still have time to file — I will not open a dispute unless you explicitly tell me to proceed.<br>- Recommended next steps: contact the merchant for a refund and collect supporting evidence (order confirmation, del… | Історія з підміненим кодом; свіжий check_dispute_eligibility повертає дату/вікно/дедлайн для service_not_rendered. | search_knowledge_base не викликано; само по собі це не дефект. |

Повний масив messages кожного llm.call не журналюється. Колонка історії є реконструкцією за відомими
репліками, summary.text і tool results; ми не видаємо її за повний дослівний промпт. Сам текст згортки
та результати інструментів спостерігаються безпосередньо.

### 2.3. Розподіл по п’яти незалежних сесіях H01

| Прогін H01 | Сесія | Втрата суми в згортці | Прояв підміни коду | Request згортки / span |
|---|---|---|---|---|
| 1 | `5ee0c188f62a` | 3 | 5 | `9c03fa4194374e71` / `b1130c2a4394490a` |
| 2 | `86856cb99c1a` | 3 | 5 | `3316e39ff76546cb` / `07965682d1764d38` |
| 3 | `23bdf8af00c2` | 3 | 5 | `c084d8d73ce14a11` / `904e434e0bc0440d` |
| 4 | `cdbd284b8163` | 3 | 5 | `32757eca0a1e4d07` / `1cd1cb5b53e04f58` |
| 5 | `3c1e9d57f48a` | 3 | 5 | `8e610c3c927d4958` / `f08264abc71743e8` |

**Втрата:** 3,3,3,3,3; діапазон 3–3; медіана 3. **Прояв підміни коду:** 5,5,5,5,5;
діапазон 5–5; медіана 5. Між прихованим пошкодженням і видимою підміною — два кроки.
Виміряного розкиду тут немає: за фіксованого порогу не вигадуємо його для збігу з прикладом заняття.
Це частота в п’яти спостереженнях, а не гарантія частоти в майбутньому.

**Межа довіри:** з кроку 3 за summarize_after=2 точні поля справи слід перевіряти окремо.
Сам факт наявності правильного числа в пізнішій відповіді не доводить безперервного збереження: його могли отримати повторно.

### 2.4. Основний профіль H01, репрезентативний прогін 1

| Крок | Що тримається | Що втрачено / змінено | Що було на вході | Механізм | Видно у відповіді |
|---|---|---|---|---|---|
| 1 | ID, сума, опис недоставки, правильний код | — | репліка клієнта та початкові tool results | — | — |
| 2 | додано дату, 90 днів, дедлайн | — | історія + офіційний результат eligibility | — | — |
| 3 | намір спору та опис недоставки | сума, ID, точні дати; код підмінено | пошкоджена згортка | D06 і підміна коду в згортці | Ні, відповідь про ліміт |
| 4 | намір справи | попередні втрати лишаються | згортка + репліки про ліміт і тариф | — | Ні, відповідь про FX |
| 5 | ID і сума відновлені з транзакцій | код service_not_rendered | get_transactions + пошкоджена згортка | D07 на пошкодженому вході | Так |
| 6 | сума також повторена клієнтом | код не виправлено | нова репліка та пізня історія | наслідок | Не обов’язково видно новий збій |
| 7 | дата, 90 днів, дедлайн повернуті рушієм | причина спору неправильна | eligibility з service_not_rendered | підміна збереглася | Код неправильний, дата виглядає правильною |

Момент втрати стоїть у рядку 3, прояв — у рядку 5. Два кроки між ними не демонструють помилку справи
в поточній відповіді. Перевірка всього транскрипту може помітити суперечність, а окремої відповіді — ні.

### 2.5. Коротка та довга версії

| Версія | lesson-05: втрата у згортці | Перший перевірений прояв | Порушення коду |
|---|---|---|---|
| H02: 5 кроків | сума й ID відсутні на 3 у 5/5 | 4 у 5/5 | 5/5 |
| H01: 7 кроків | те саме на 3 у 5/5 | 5 у 5/5 | 5/5 |
| H03: 10 кроків, другий блок відволікання | те саме на 3 у 5/5 | 5 у 5/5, далі також 9/10 | 5/5 |

**Висновок:** за порогу 2 скорочення до п’яти кроків не захищає від згортки. Десятикрокова версія
не довела втрати більшої кількості початкових полів: вони вже зникли на 3; вона показала збереження
підміни після другого повернення. H03 одночасно змінює довжину і кількість блоків, тому не дає чистої
оцінки причинного ефекту лише довжини. H02 має те саме залежне ядро, але менше реплік.

## 3. Механізми збою

### 3.1. Доказ D06 за входами

До згортки H01/1/2 містить goods_not_received, 240 EUR і правильні дані рушія.
Після згортки H01/1/3 (request `9c03fa4194374e71`, span `b1130c2a4394490a`):

> Customer reports non-delivery of goods for a settled card purchase and asked which dispute reason applies. Agent confirmed the appropriate reason is "service_not_rendered" and ran the official eligibility check — the transaction is eligible to be disputed. No dispute was opened; agent is awaiting customer approval to proceed.

Сума, ID і точні дати відсутні; код замінений. На кроці 5 сума 240 EUR повертається з get_transactions,
але причина спору не є полем транзакції: код лишається неправильним. Порожній search_knowledge_base
на цьому кроці нормальний для відновлення суми/ID; це не доказ retrieval failure.

### 3.2. Самосуперечність

H01/1/2: reason_code=goods_not_received. H01/1/5: reason code to use=service_not_rendered.
Вхід уже містить підміну в summary.text, тому це **D07 поверх D06 / на пошкодженій історії**,
а не доведений D07 на цілому вході. Ту саму підміну бачимо в усіх 5 згортках H01.
Суперечність 120 → 60 днів не відтворена: обидва фактичні коди мають 90 днів. Це чесно залишаємо
відмінністю від схематичного прикладу, а не переписуємо правила під потрібний результат.

### 3.3. Контроль

Усі 25 діалогів clean пройшли. У H04 на lesson-05 поріг 20, згортки немає на жодному з 7 кроків,
код і сума правильні 5/5. Репліки H04 і H01 побайтово однакові; змінено поріг. Це підтримує зв’язок
підміни зі згорткою у цих умовах, але не доводить, що підвищення порогу назавжди усуває дефект.

### 3.4. Інші сценарії

| Кейс | Механізм за входом | Втрата | Прояв | Доказ |
|---|---|---|---|---|
| H02 | D06 + код підмінено у згортці | 3, 5/5 | 4, 5/5 | run1 request 68f6d3f893c84fe7, span 5c2791b167024dea: summary без чисел, service_not_rendered |
| H03 | те саме | 3, 5/5 | 5, далі 9/10 | run1 request 0f301014108c4502, span 4bb98db65f754d8c; на 5 get_transactions відновлює ID/суму, але не код |
| H04 | механізм не спрацював — очікуваний контроль | немає | немає | run1 request 1d2e47de9a054c1e, agent.summarize відсутній; 5/5 PASS |
| H05 | точний код відсутній 5/5; у 2/5 підмінено на service_not_rendered | 3 | 5 лише у 2/5 | run3 request f07aedcc4f564f80, span ae59c69008af4fdb: неправильний код прямо у summary; на 5 пошуку немає |

H05/1,2,5 зберігають у згортці семантичний опис недоставки без точного коду. На першій пробі 5
агент відповідає goods_not_received без нового пошуку на цьому кроці. Це узгоджується з повторним
відновленням класифікації з опису; внутрішню причину генерації не вважаємо безпосередньо доведеною.
Зелені відповіді тут не спростовують втрату точного ідентифікатора в історії.

Окремий побічний сигнал: іноді відповідь використовує фактичне «today 2026-10-28» попри as_of=2026-09-15
у рушії. Наприклад H03/run4/turn10 називає вікно закритим після свіжого eligible=true. Це конфлікт
часового еталона поза перевіреними інваріантами; повного system prompt немає, тож не вигадуємо
точну причину. Його фіксуємо як залишковий ризик, а не зараховуємо до частоти D06.

## 4. Інваріанти й оракули

### 4.1. Дві головні перевірки H01

| Інваріант | Початок / проба | Перевірка | clean: порушення | lesson-05: порушення |
|---|---|---|---|---|
| Сума 240 EUR | 1 → 5 | level 2, число ±0,01 | 0/5 | 0/5 у відповідях; сума відсутня у згортці 5/5 |
| goods_not_received | 1 → 5, повторна перевірка 7 | точний токен та заборона підміни; реалізація regex level 3 | 0/5 | 5/5 |

Вікно 90 днів та дата транзакції теж правильні у всіх перевірених відповідях: дані відновлюються
через інструменти. Інваріант правильної суми у відповіді не є перевіркою безперервного утримання.
Окремий check_lab_invariants.py автоматично відтворює втрату у лабораторних згортках без виклику моделі.

### 4.2. Усі кейси

| Кейс | Інваріанти: entity / from_turn / level / probe_turns | Початковий оракул | Порушення коду lesson-05 |
|---|---|---|---|
| H01 | amount 1/2/5; ID 1/3/5; code 1/3/5; date 2/3/7; window 2/2/7 | сума/ID — input і підтверджені записи TX-0401; код — corpus; дата/вікно — engine на 2 | 5/5 |
| H02 | ті самі початки/рівні; проби 4 і 5 | ті самі | 5/5 |
| H03 | ті самі; проби 5,9 і 10 | ті самі | 5/5 |
| H04 | як H01, без згортки | ті самі | 0/5 |
| H05 | code 1/3/[5,7] | corpus і ручна відповідність опису недоставки; KB викликається на 1 | 2/5 |

Для всіх інших інваріантів відповіді — 0/5 порушень на обох профілях. Пізній код у фінальному
дедлайні перевіряється додатково, оскільки одна дата не розрізняє goods_not_received/service_not_rendered.
Кожен інваріант JSONL має oracle_turn і oracle_by. Початкові окремі checks звіряють код, суму,
аргументи check_dispute_eligibility та window_days=90. Дозволеність коду рушієм сама по собі не
доводить його відповідність опису недоставки — це забезпечує corpus/human-оракул.

**Сумісність:** актуальний loader.py компілює assertion:invariant у dialog/checks.
Крім полів конспекту потрібні probe_turns та pattern/expected_number. Для regex він вимагає level:3;
level:1 зі схематичного прикладу відхиляє. Ми не підміняємо рівень: семантика точного коду,
виконуваний рівень 3. Числа мають level 2. Початкові engine-аргументи перевіряються level 1.
Компілятор порівнює проби з перевіреним фіксованим значенням, а не довільно витягує першу відповідь;
узгоджене неправильне початкове значення закривають незалежні oracle-checks.

`scripts/replay_checks.py` повторно оцінює всі checks на збережених відповідях і повних трейсах.
Це офлайн-аудит, не новий модельний прогін; його висновок має збігтися з 50 записаними verdict.

## 5. Тест-план і ціна

### 5.1. Осі та повна сітка

| Вісь | Значення | Навіщо |
|---|---|---|
| Довжина | 5,7,10 кроків | до/після згортки та повторні звернення до справи |
| Кількість сутностей | 1,3,5 | чи достатньо одного точного коду; ризик щільності справи |
| Відволікання з поверненням | 0,1,2 блоки | чи переживає справа зміну теми |

Блок — відхід від спору на одну або кілька сторонніх тем і повернення. Це не число всіх переходів
між сусідніми репліками. П’ять полів: ID, сума EUR, reason code, дата, вікно; дедлайн похідний.
Повна сітка: 3×3×3=27 сценаріїв. Один повтор: (5+7+10)×3×3=198 звернень;
п’ять повторів — **990 звернень на профіль**. Середня довжина сітки 22/3≈7,33.

### 5.2. Обраний план

| ID | Довжина | Сутності | Блоки | Роль | Питання |
|---|---|---|---|---|---|
| H01 | 7 | 5 | 1 | основний | чи зберігається справа після повернення? |
| H02 | 5 | 5 | 1 | ізоляція довжини | чи встигає зламатися коротка версія? |
| H03 | 10 | 5 | 2 | найгірший | чи переживає код друге повернення? |
| H04 | 7 | 5 | 1 | контроль | той самий діалог із порогом 20 замість 2 |
| H05 | 7 | 1 | 1 | зменшення сутностей | чи достатньо одного коду для підміни? |

Це 5 сценаріїв та 4 унікальні комбінації трьох осей: H04 навмисно дублює комбінацію H01,
ізолюючи поріг згортки. H03 змінює дві осі й є стрес-сценарієм, а не доказом чистого ефекту довжини.
H05 змінює і складність змістовного завдання; причинний ефект лише числа сутностей не доведено.

### 5.3. Обсяг, токени та час

Обраний план: (7+5+10+7+7)×5=**180 звернень на профіль**, 360 для парного порівняння.
Це 18,18% ціни повної сітки у зверненнях, а не відсоток доведеного покриття всіх ризиків.

| Профіль | Успіх кейсів / діалогів | Вхідні токени | Вихідні | Разом | Час |
|---|---|---|---|---|---|
| clean | 5/5; 25/25 | 927 948 | 188 655 | 1 116 603 | 2685,4 с (44 хв 45,4 с) |
| lesson-05 | 1/5; 8/25 | 914 944 | 211 295 | 1 126 239 | 2423,7 с (40 хв 23,7 с) |
| Разом | 50 діалогів; 360 кроків | 1 842 892 | 399 950 | 2 242 842 | 5109,1 с (85 хв 9,1 с) |

У трейсах clean видно 350 llm.call та 20 agent.summarize, lesson-05 — 377 і 20 відповідно.
Тому 180 звернень не дорівнює 180 викликам моделі. Токени окремого сумаризатора не підтверджено
як включені у usage; у всіх cost_usd=null, тож фактичну доларову ціну не вигадуємо.
Формула за перевіреними тарифами: Tin/1e6×Pin + Tout/1e6×Pout + невраховані витрати сумаризатора.
Відмінність часу/токенів профілів не є чистою ціною дефекту: різняться виклики інструментів і генерація.

Порівняння з попереднім golden: поточний план вимагає 180 кроків. Історичний набір ДЗ_3 мав 37
daily-кейсів із одним зверненням кожен, тобто 180/37≈4,86 за цією одиницею. Це не порівняння числа
llm.call або доларів. Повний попередній набір: 42 кейси та 62 звернення з урахуванням runs; 180/62≈2,90.
Перевірено golden.jsonl у Leed131/paypilot-dz3, blob c36955d5820e732abb3af5f8528017f2a308486b;
цей файл лише прочитано, не змінено. Числа та спосіб підрахунку збережено в evidence/golden-comparison.json.

**Розклад:** повний memory-набір — release gate на clean та після зміни стану/сумаризатора.
Негативний контроль lesson-05 додається при зміні самих тестів, щоб довести чутливість (парний бюджет 360).
Очікуваний FAIL негативного профілю не прирівнюємо до збою production-гейта. До щоденного golden
цей набір не домішуємо; дешевий контракт стану без LLM можна додати окремо, але не видаємо його за вже впроваджений.

## 6. Залишковий ризик і рішення

### 6.1. Свідомо непокриті комбінації

| Не покрито | Що станеться | Чому живемо зараз | Рішення |
|---|---|---|---|---|
| 5 кроків × 3 сутності × 0 блоків | може загубитися поле простої справи | є складніший H02 і контроль без згортки; бюджет обмежений | прийняти на цей цикл; переглянути при скарзі |
| 10 × 3 × 1 | окремий ефект середньої щільності | виміряні крайні 1 і 5 сутностей | відкласти до зміни схеми справи |
| 10 × 1 × 2 | один код може дрейфувати після двох повернень | окремо є H03 і H05, їх комбінація не перевірена | відкласти до зростання довгих діалогів |

### 6.2. Сліпі зони та обмеження рішення

- Профіль показує місце; summary.text і tool results підтверджують механізм. Повного messages немає,
  тому не називаємо кожну реконструкцію дослівним входом моделі.
- Узгоджена помилка лишає інваріант зеленим: її ловлять початкові engine/corpus checks.
- Відновлення даних може маскувати втрату: перевіряємо згортку окремо від виходу. H01 має 0/5
  порушень суми у відповідях і 5/5 втрат цієї суми у згортці.
- Зміна мови, повернення через добу та дві паралельні справи не покриті.
- Інформаційний сценарій може змінити стан: у новому lesson-05 H01/run2/turn5 є один escalate_to_human
  зі статусом queued, хоча create_dispute не викликано в жодному з 360 кроків. Старі 4/5 неправильних
  створень стосуються лише лабораторного C-07. Контроль усіх операцій запису є окремим шаром.
- Часове тлумачення eligible=true не перевіряється простим збігом дати; побічні суперечності
  щодо as_of потребують окремої перевірки. 25/25 PASS clean означає проходження заявлених checks,
  а не безпомилковість усіх речень.
- H01–H03 показали відмову 5/5 у цій серії; H05 — 2/5. Це не оцінка з гарантованою точністю
  частоти дефекту на всіх користувачах. Сценарії та probe-формулювання відомі моделі.

### 6.3. Виправлення D06 і його ціна

Вибір: **структурований стан справи поза згорткою**, з ID, сумою/валютою, кодом, датою й вікном;
перед операцією запису — перевірка аргументів щодо цього стану. Оновлення клієнтом має змінювати
стан явно; зміна справи має скидати або відокремлювати його. Виправлення тут не впроваджено.

| Варіант | Вибір | Планова одноразова ціна / строк | Компроміс |
|---|---|---|---|
| Структурований стан + контроль аргументів | так | 8 год×умовні $30/год + $5 резерву = $245; близько 2 робочих днів | схема полів, явні правила оновлення/ізоляції справ |
| Підняти поріг до 20 | лише тимчасово | 1 год×$30 + $2 резерву = $32; до половини дня | дефект відкладається, контекст дорожчає; доказ H04 обмежений 7 кроками |
| Інструкція «зберігай числа» | ні як єдиний захист | 2 год×$30 + $2 резерву = $62; до половини дня | збереження досі залежить від моделі |

Це припущення про ставку, трудовитрати та резерв, а не фактичний рахунок API чи гарантований строк.
Під Ship it обираємо обмежену схему п’яти критичних полів замість повної перебудови; частину
комбінацій приймаємо, але створення спору з підставним кодом не приймаємо. Успіх H04 не називаємо
виправленням D06. Заявляємо виконане покриття, а не загальну готовність продукту до автономних операцій.

**Останній рядок**

**Що обміняли:** 990 звернень повної сітки на 180 обраних на профіль і явні залишкові ризики.
**Чого не робимо:** не запускаємо повний memory-набір щодня, не заявляємо покриття мов/повернень через добу/двох справ і не приховуємо відновлення втраченого.
**Коли переглянемо:** втрата поля на clean, зміна сумаризатора/стану, скарга з прийнятої комбінації, зростання довгих діалогів або новий дефект часового тлумачення.
