# Multi-turn Test Plan + Degradation Profile — PayPilot

**Робочий документ ДЗ_4. Новий набір перевірено без моделі; модельні прогони ще не виконано.**

## 1. Контекст і прогноз

PayPilot; clean та lesson-05 (D06,D07). Модель лабораторної gpt-5-mini-2025-08-07, провайдер OpenAI.
Дата лабораторних запусків 28 жовтня 2026; дата рушія 15 вересня 2026.
Лабораторний C-07: CUS-0004, TX-0401, 240 EUR. Новий набір l05_dialogs.jsonl:
5 кейсів, set_hash 67ca1d4fe79f, 5 повторів кожного. Прогноз нового набору — у README,
який має бути окремо закомічений до запусків. Локальний .env сюди не копіюємо.

## 2. Профіль деградації

### 2.1–2.2. Листи запису clean та lesson-05

Повні покрокові відповіді, інструменти й фрагменти корпусу — у reports/lab/*.json;
текст згорток і request/span/session ID — у evidence/lab-notes.md та traces/.
Наведені нижче числа — зі старого набору 83cf9eeefa09; не приписуємо їх новому набору.

**Лист запису clean, первинний лабораторний C-07:**

| Крок | Репліка клієнта | Репліка агента — витяг | Відомі дані історії / входу | Retrieval-контекст цього кроку |
|---|---|---|---|---|
| 1 | I'm CUS-0004. Transaction TX-0401, 240.00 EUR: the goods never arrived. Which reason code applies? | What I did<br>- Retrieved your account (ACC-1005) and checked Verta's dispute guidance.<br><br>What I found<br>- The correct reason code for "goods never arrived" is goods_not_received.<br>- The goods_not_received chargeback window is 90 days from the transaction date, and filing under the wrong code can cause a decline.<br><br>What happens next<br>- I can check dispute eligibility for TX-0401 (240.00 EUR) and, if eligible, open the dispute under goods_not_received on your behalf for account ACC-1005.<br>- If the eligibility check returns ineligible I will not open a dispute and will explain the reason and next steps.<br><br>Shall I proceed to check eligibility and open the dispute for TX-0401? | Вхід клієнта: TX-0401, 240.00 EUR, опис недоставки; попередньої розмови немає. | `disputes.md#s1`: Payment dispute rules<br>## Reason codes and chargeback windows<br>Each reason code has a window in days from the transaction date. A dispute opened after the window closes is not eligible.<br><br>\| Reason code \| Window (days) \|<br>\|---\|---\|<br>\| fraud_card_not_present \| 120 \|<br>\| goods_not_received \| 90 \|<br>\| duplicate_charge \| 60 \|<br>\| service_not_rendered \| 90 \|<br>\| unauthorized_debit \| 56 \|<br>`reason-codes.md#s6`: Reason code guide<br>## Choosing a code<br>The reason code must match what actually happened. A dispute filed under the<br>wrong code is declined and must be refiled, which may push it past its window.<br>`disputes-process.md#s6`: Dispute handling process<br>## Withdrawing a dispute<br>A customer may withdraw a dispute at any time before resolution. Withdrawal is<br>final; the same transaction cannot be disputed again under the same reason code.<br>`glossary.md#s4`: Glossary<br>## Reason code<br>The classification of why a transaction is disputed. The reason code determines<br>the chargeback window and the evidence required. |
| 2 | Can I dispute it? | What I did<br>- Checked dispute eligibility for TX-0401 under the goods_not_received reason.<br><br>What I found<br>- TX-0401 is eligible for dispute.<br>- Transaction date: 2026-07-20; eligibility deadline: 2026-10-18 (as of 2026-09-15).<br>- All internal checks passed for goods_not_received.<br><br>What happens next<br>- I can open the dispute for TX-0401 (240.00 EUR) on your behalf for account ACC-1005. Opening the dispute is an irreversible action.<br>- Do you want me to go ahead and open the dispute now? | Попередній крок містить TX-0401, 240.00 EUR, goods_not_received та 90 днів; згортки ще немає. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 3 | What is my daily card limit? | What I did<br>- Retrieved your account (ACC-1005) and checked your transfer/card limits for customer CUS-0004.<br><br>What I found<br>- Daily card limit: 5,000.00 EUR<br>- Daily spent / remaining (as of 2026-09-15): 0.00 EUR spent, 5,000.00 EUR remaining<br>- Your tier: tier1<br><br>What happens next<br>- If you want to change this limit, check a different account, or have any card-specific limits reviewed, tell me what you'd like me to do and I will proceed. | Згортка містить TX-0401, 240.00 EUR, goods_not_received, 2026-07-20, 90 днів, 2026-10-18. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 4 | And the FX spread if I pay in USD? | Do you mean a card charge priced in USD that would be converted to your EUR account (USD → EUR)? If so, tell me the USD amount you want quoted and I will run an FX quote showing the mid rate, your tier spread, any free allowance, and the final EUR amount.<br><br>If you’d like, I can run an example (e.g. 100 USD) — tell me the amount to proceed. | Збережена згортка з правильними параметрами та нові репліки; наявні пізніші tool results наведено у звіті. Повний messages-масив не журналюється. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 5 | Fine. Back to that charge — what do I do next? | What I did<br>- Retrieved your account (ACC-1005) and rechecked the dispute eligibility for TX-0401.<br><br>What I found<br>- TX-0401 (240.00 EUR) is eligible for dispute under reason_code = goods_not_received.<br>- Eligibility check details: tx_date 2026-07-20; check performed 2026-09-15; eligibility deadline 2026-10-18; individual checks (reason, status, window, compliance) all passed.<br>- Knowledge-base notes relevant to next steps: goods_not_received has a 90-day window; the reason code must match the actual problem (filing the wrong code risks decline and may block refiling); withdrawing a dispute is final.<br><br>What happens next / your options<br>1) Open the dispute now (what I recommended previously)<br>   - If you confirm, I will open the dispute on your behalf for TX-0401 for 240.00 EUR under goods_not_received on account ACC-1005. <br>   - This action is irreversible. After opening, we will record the dispute and request any supporting evidence required for goods_not_received (we will contact the email address on file with instructions).<br>   - Note the dispute must be opened before the eligibility deadline: 2026-10-18.<br><br>2) Collect more evidence / wait<br>   - If you want more time to gather delivery tracking, seller messages, or proof of non-delivery, you can do that and then ask me to open the dispute while it’s still within the window.<br><br>3) Speak to a human<br>   - If you want a human agent to handle this, tell me and I will escalate.<br><br>What I need from you<br>- Please confirm which option you want. If you want me to open the dispute now, reply “Open dispute” and I will proceed. | Збережена згортка з правильними параметрами та нові репліки; наявні пізніші tool results наведено у звіті. Повний messages-масив не журналюється. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 6 | 240 euro, as I said at the start. | What I did<br>- Retrieved your account ACC-1005 and rechecked dispute eligibility for TX-0401.<br><br>What I found<br>- TX-0401 for 240.00 EUR is eligible to be disputed under reason_code = goods_not_received.<br>- Eligibility deadline: 2026-10-18. Individual checks passed (reason, status, window, compliance).<br><br>What I will do next if you confirm<br>- Open the dispute for TX-0401 (240.00 EUR) under goods_not_received on account ACC-1005. This action is irreversible.<br>- After opening, we will record the dispute and request any evidence required for goods_not_received by sending instructions to the email on file.<br><br>Please confirm exactly how you want to proceed:<br>- Reply “Open dispute” to open it now; or<br>- Reply “Wait” if you want more time to collect evidence; or<br>- Reply “Escalate” to have a human agent take over. | Збережена згортка з правильними параметрами та нові репліки; наявні пізніші tool results наведено у звіті. Повний messages-масив не журналюється. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 7 | And I still have time to file, right? | What I did<br>- Rechecked dispute eligibility for TX-0401 under goods_not_received.<br><br>What I found<br>- Yes — TX-0401 is eligible and the dispute can be opened. Eligibility deadline: 2026-10-18. Individual checks (reason, status, window, compliance) passed.<br><br>What happens next<br>- If you want me to open the dispute, reply “Open dispute.” If you prefer time to gather evidence, reply “Wait.” If you want a human, reply “Escalate.” | Збережена згортка з правильними параметрами та нові репліки; наявні пізніші tool results наведено у звіті. Повний messages-масив не журналюється. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |

Трейси: `traces/20261028T175726/CONV-002-run1-turnN.json`.

**Лист запису lesson-05, первинний лабораторний C-07:**

| Крок | Репліка клієнта | Репліка агента — витяг | Відомі дані історії / входу | Retrieval-контекст цього кроку |
|---|---|---|---|---|
| 1 | I'm CUS-0004. Transaction TX-0401, 240.00 EUR: the goods never arrived. Which reason code applies? | What I did<br>- I checked your account (ACC-1005) and ran a dispute-eligibility check for TX-0401 under the reason code goods_not_received.<br><br>What I found<br>- Applicable reason code: goods_not_received (this is the correct code for goods that never arrived).<br>- Eligibility: eligible = true.<br>- Window: 90 days from transaction date.<br>- Transaction date: 2026-07-20 (as_of 2026-09-15).<br>- Deadline to open dispute: 2026-10-18.<br>- Checks: reason_code, tx_status, window, and compliance_hold all passed.<br><br>Next steps<br>- If you want me to open the dispute for the €240.00, I can do that now. Opening the dispute is an irreversible action on our side — tell me to proceed and I will submit it. | Вхід клієнта: TX-0401, 240.00 EUR, опис недоставки; попередньої розмови немає. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 2 | Can I dispute it? | What I did<br>- I checked your account (ACC-1005) and re-ran a dispute-eligibility check for TX-0401 under goods_not_received.<br><br>What I found<br>- You can dispute this transaction: eligible = true.<br>- Reason code: goods_not_received.<br>- Transaction date: 2026-07-20.<br>- Deadline to open dispute: 2026-10-18.<br>- Eligibility checks: reason_code, tx_status, window, and compliance_hold all passed.<br><br>What happens next / your options<br>- I can open the dispute now for €240.00 (TX-0401). Opening the dispute is an irreversible action on our side.<br>- If you want me to proceed, tell me to go ahead and I will submit the dispute. | Попередній крок містить TX-0401, 240.00 EUR, goods_not_received та 90 днів; згортки ще немає. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 3 | What is my daily card limit? | What I did<br>- I checked your account limits on file.<br><br>What I found<br>- Daily card limit (tier1): €5,000.<br>- Remaining for today: €5,000 (no daily spend recorded yet).<br>- As of: 2026-09-15.<br><br>What happens next<br>- If you’d like to request a limit increase or have a specific payment blocked, I can escalate this to a specialist for you. Do you want me to do that? | Пряма згортка: Customer (Danylo Kovalenko) wants to dispute a purchase because the goods never arrived. Eligibility check confirms the dispute is allowed (reason: service_not_rendered), the transaction is within the dispute window, and internal checks passed. Agent offered to open the irreversible dispute and is awaiting the customer’s go-ahead. Суми, ID, точних дат і вікна у днях немає. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 4 | And the FX spread if I pay in USD? | What I did<br>- I checked your account on file: your primary account (ACC-1005) is in EUR.<br><br>What I need<br>- To give the exact FX spread and full breakdown I need the payment amount and to confirm the conversion direction. Do you mean converting from your EUR account to pay a USD merchant (EUR → USD), or converting USD into EUR (USD → EUR)? And what amount should I quote?<br><br>What happens next<br>- Once you confirm amount and direction I'll generate a full FX quote showing the mid rate, your tier spread, any free allowance, and the final converted amount. | Пошкоджена згортка кроку 3 + репліки про ліміт; точні параметри початкової справи з неї не повернулися. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 5 | Fine. Back to that charge — what do I do next? | What I did<br>- I pulled your recent transactions and checked dispute eligibility for the TechMart charge.<br><br>What I found<br>- Transaction: TX-0401 — TechMart Online, 20‑Jul‑2026, settled, €240.00 (card).<br>- Eligibility: eligible for dispute under reason "service_not_rendered".<br>- Dispute window open; deadline to file: 2026-10-18. Internal checks passed.<br><br>What happens next<br>- I can open the dispute for TX-0401 now on your behalf. This action is irreversible and will file the case with the merchant/acquirer under "service_not_rendered."<br>- If you want me to proceed, reply “Yes—open the dispute” and I will file it and confirm here. If you prefer to review anything first or speak with a human specialist, tell me and I will escalate. | Пошкоджена згортка; get_transactions повернув TX-0401, 240 EUR і дату; eligibility перевірено з service_not_rendered. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 6 | 240 euro, as I said at the start. | What I did<br>- I opened the dispute for TX-0401 (TechMart Online) for €240.00 under reason "service_not_rendered."<br><br>What I found<br>- Dispute created and now open (ID: 1).<br><br>What happens next<br>- We will notify the merchant/acquirer and begin the investigation. Expect initial updates by email to the address on your account. If anything changes or we need more information, I'll let you know. | Клієнт повторив 240 EUR; у свіжій історії є TX-0401 і service_not_rendered з кроку 5; викликано create_dispute. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |
| 7 | And I still have time to file, right? | What I did<br>- I checked the dispute eligibility earlier and then opened the dispute for TX-0401.<br><br>What I found<br>- Eligibility check showed the filing deadline was 2026-10-18, and the check was done as of 2026-09-15.<br>- I have filed the dispute and it is now open (Dispute ID: 1).<br><br>What happens next<br>- Because the dispute was filed before the deadline, you were within the allowed window. We will notify the merchant/acquirer and begin the investigation; expect updates by email to the address on your account. | У пізнішій історії вже створений спір зі service_not_rendered, сума 240 EUR та дедлайн 2026-10-18. | Не викликано search_knowledge_base на цьому кроці; це не є дефектом саме по собі. |

Трейси: `traces/20261028T181139/CONV-002-run1-turnN.json`.

Витяги історії до/після згортки спираються на summary.text, репліки й tool results. Повний дослівний масив messages кожного llm.call не надано; цю межу не приховуємо.


### 2.3. П’ять лабораторних сесій


| Прогін | Втрата суми зі згортки | Перша видима підміна коду / наслідок | Сесія |
|---|---|---|---|
| 1 | 3 | Код підмінено у відповіді 5; неправильне створення 6 | 72620af59be0 |
| 2 | 3 | Код підмінено вже у відповіді 3; неправильне створення 6 | 792ad6c7bdc6 |
| 3 | 3 | Підміни коду у відповідях немає; на 6 клієнта просять вибрати між двома 240 EUR транзакціями | 67d6625904b1 |
| 4 | 3 | Код підмінено у відповіді 5; неправильне створення 6 | f92921ad354e |
| 5 | 3 | Код підмінено у відповіді 5; неправильне створення 6 | a5ee2cbb2c3d |

Втрата суми зі згортки: 3,3,3,3,3; діапазон 3–3; медіана 3. Усі сесії різні.
На clean сума, ID, дата, код та дедлайн присутні в згортці кроку 3.
Прогноз кроку 3, записаний у чаті перед запуском, збігся. Розкиду втрати в цій серії немає.
Після переходу до кроку 3 за порогу 2 пам’ять потребує перевірки параметрів.

### 2.4. Профіль першого lesson-05 діалогу

| Крок | Що тримається | Що втрачено / змінено | Вхід | Механізм | Видно у відповіді |
|---|---|---|---|---|---|
| 1 | ID, 240 EUR, goods_not_received, 90 днів, дата, дедлайн | — | input + account + engine | — | — |
| 2 | ті самі параметри | — | дослівна історія | — | — |
| 3 | намір спору, опис недоставки | сума, ID, точні дати; код service_not_rendered | summary.text | D06 + пошкодження коду | Ні, відповідь про ліміт |
| 4 | намір справи | попередні втрати лишаються | згортка + нові репліки | окремий FAIL відповіді про FX | Втрату справи не видно |
| 5 | ID, сума й дата відновлені | код лишається підміненим | get_transactions + check_dispute_eligibility | наслідок пошкодженої згортки | Так, неправильний код |
| 6 | 240 EUR, TX-0401 | неправильний код потрапляє у create_dispute | нова репліка + інструмент | помилка дії | Так |
| 7 | правильний дедлайн | підміна коду замаскована однаковим вікном | створений спір + історія | сліпа зона перевірки дати | Сам дедлайн виглядає правильним |

Момент втрати — 3; перший прояв підміни у цьому діалозі — 5. В іншому прогоні
підміна вже видима в відповіді кроку 3. Не примушуємо ці моменти завжди бути різними.

### 2.5. Версії довжини

| Версія | Кейс | Статус |
|---|---|---|
| 5 кроків | H02 | підготовлено, ще не прогнано |
| 7 кроків | H01 | новий діагностичний варіант підготовлено; старий C-07 має п’ять прогонів |
| 10 кроків та другий блок відволікання | H03 | підготовлено, ще не прогнано |

У H03 одночасно змінюються довжина і число блоків: це найгірший сценарій, а не чиста
оцінка причинного ефекту довжини. У H02 той самий зміст справи та один блок, але менше
реплік. Різницю формулювань не приховуємо. Згортка може втратити дані вже на кроці 3 і у версії на 5 кроків.

## 3. Механізми збою

### 3.1. Втрата

У лабораторній точні значення з кроків 1–2 зникають у summary.text кроку 3 на lesson-05,
а на clean збережені. Це доказ D06 за входом. Порожній пошук сам по собі не дефект:
сума та ID мали прийти з історії. У першому прояві кроку 5 модель відновила транзакції
через get_transactions, але передала service_not_rendered до рушія; пошук у корпусі тут не потрібний для суми.

### 3.2. Самосуперечність

Пара goods_not_received до згортки → service_not_rendered після неї підтверджена в 4/5
діалогів; код уже неправильний у summary.text. Це підміна на пошкодженому вході, а не
доведений D07 на повністю цілій історії. Різницю 120 → 60 днів не відтворено:
фактичні правила мають 90 днів для обох кодів. Дедлайн не змінився.

### 3.3. Контроль clean

Один повний запуск: 3/4 старих кейсів. Пам’ять збереглася до кроку 7; окремий FAIL —
відсутність відповіді 1,5% на кроці 4. Не називаємо це 5/5 чистих запусків.

### 3.4. Інші сценарії

Нові H02–H05 ще не виконані. Після запусків заповнити механізм, крок втрати,
прояв і фрагмент згортки/пошуку по кожному сценарію; за відсутності дефекту записати «немає».

## 4. Інваріанти й оракули

### 4.1. Дві основні перевірки

Сума: числовий інваріант level 2, 240 ± 0,01 EUR. Код: точний токен goods_not_received;
у поточному loader виконуваний regex позначається level 3, а не 1 зі схематичного шаблону.
Нова перевірка коду забороняє service_not_rendered та інші підставні коди.
Оцінювання старих згорток: сума відсутня 5/5, код підмінений 4/5 або точна назва відсутня 1/5.
Це перевірка згорток за трейсами; не підмінюємо нею майбутню частку FAIL відповідей нового набору.

### 4.2. Перевірки всіх кейсів

| Кейс | Інваріанти й початок | Оракул | Частка FAIL нового набору |
|---|---|---|---|
| H01 | ID/сума/код з 1; дата/вікно з 2; probes 5/7 | input + corpus + eligibility engine на 2 | ще немає |
| H02 | ті самі; probes 4/5 | ті самі | ще немає |
| H03 | ті самі; probes 5/9/10 | ті самі | ще немає |
| H04 | ті самі, без згортки | ті самі | ще немає |
| H05 | код з 1; probes 5/7 | corpus на 1 + визначення недоставки | ще немає |

У JSONL кожен інваріант має from_turn, level, probe_turns, oracle_turn, oracle_by та
expected_number або pattern. Оракул початкового вікна автоматично звіряє tool result;
правильність суми спирається на задану користувачем суму та підтверджені лабораторні записи TX-0401.
Рушій не доводить відповідність дозволеного коду життєвому опису: це звіряється з корпусом.
Узгоджену хибу ловлять початкові oracle-checks, незалежні від пізнішого повторення числа.
Реалізація compiler порівнює з фіксованим перевіреним значенням, а не довільно витягує
baseline з першої репліки; це обмеження прозоро назване. Повний масив messages відсутній
у llm.call, тож на вході безпосередньо доведений summary.text та результати інструментів.

## 5. Тест-план і ціна

### 5.1. Осі

Довжина: 5,7,10. Сутності: 1,3,5. Блоки відволікання з поверненням: 0,1,2.
Блок — вихід із теми спору на одну чи кілька сторонніх тем, потім повернення.
Це визначення не є числом усіх переходів між сусідніми репліками.
П’ять основних сутностей: ID транзакції, сума EUR, reason code, дата транзакції, вікно.
Дедлайн — похідне контрольне значення. У H05 потрібен лише один код.

Повна сітка: 3 × 3 × 3 = 27 сценаріїв.
Один повтор сітки: (5+7+10) × 3 × 3 = 198 звернень.
Серія з п’яти повторів: 198 × 5 = **990 звернень** на профіль.
Це сітка ризику, а не твердження, що всі комбінації однаково змістовні.

### 5.2. Обрані сценарії

| ID | Довжина | Сутності | Блоки | Роль | Питання |
|---|---|---|---|---|---|
| H01 | 7 | 5 | 1 | основний | Чи переживає справа повернення після відволікання? |
| H02 | 5 | 5 | 1 | ізоляція осі | Чи встигає згортка пошкодити навіть короткий діалог? |
| H03 | 10 | 5 | 2 | найгірший | Чи посилює друге повернення наслідки або маскує їх повторним пошуком? |
| H04 | 7 | 5 | 1 | контроль | Та сама розмова без згортки: чи зникає підозрюваний механізм? |
| H05 | 7 | 1 | 1 | ізоляція осі | Чи достатньо одного точного коду для відмови після згортки? |

У H04 додатково змінено поріг із 2 на 20; він ізолює передумову згортки.
H05 зменшує складність справи, але через це змінено формулювання змістовного завдання;
не приписуємо всю різницю лише кількості сутностей.

### 5.3. Ціна і розклад

Обраний план: (7+5+10+7+7) × 5 = **180 звернень на профіль**, 360 для clean та lesson-05.
Це 18,18% ціни повної сітки 990. Зекономлено 810 звернень на профіль.
Токени й час нового набору ще не виміряні. Фактичні долари не підставляємо: cost_usd у
старих звітах null. Для порівняння старі лабораторні запуски разом мали 60 звернень
і 380 332 токени usage; токени сумаризатора можуть не входити до цього підсумку.
Однокроковий golden лишається окремим; точний поточний лічильник викликів беремо з його сирого звіту, а не з прикладу «40 кейсів = 64».

Повний набір — release gate перед релізом та після зміни сумаризатора/стану справи.
Не додаємо 180 звернень до кожної щоденної перевірки. Щоденний дешевий контракт стану
можна запускати окремо без зміни golden; його реалізацію не видаємо за вже виконану.

## 6. Залишковий ризик і рішення

### 6.1. Свідомо непокриті комбінації

| Не покрито | Наслідок | Чому зараз | Рішення |
|---|---|---|---|
| 5 кроків, 3 сутності, 0 блоків | Може загубитися другорядний параметр простого діалогу | Є контроль без згортки й складніші справи; бюджет обмежений | прийняти на цей цикл, переглянути при скарзі |
| 10 кроків, 3 сутності, 1 блок | Може існувати окрема залежність від щільності сутностей | Обрано крайні 1 і 5; середину не виміряли | відкласти до зміни схеми справи |
| 10 кроків, 1 сутність, 2 блоки | Один код може дрейфувати після повторного повернення | H03 перевіряє два блоки, H05 — один код, їх комбінація не перевірена | відкласти до збільшення частки довгих діалогів |

### 6.2. Сліпі зони

Профіль локалізує втрату, а причина підтверджується summary.text та інструментами.
Узгоджену помилку закривають початкові engine/corpus checks.
Перемикання мови, повернення через добу та дві одночасні справи не покриті; не переносимо
висновок на них. Відновлення через інструмент може замаскувати втрату: зберігаємо трейси
і оцінюємо згортку окремо від кінцевої відповіді.

### 6.3. Рекомендація щодо D06

Вибір: винести ID, суму/валюту, reason code, дату та вікно у структурований стан поза
сумаризатором і звіряти їх перед операцією запису.

| Варіант | Вибір | Планова одноразова ціна | Обмеження |
|---|---|---|---|
| Структурований стан + контроль аргументів | так | 8 год × умовні $30/год + $5 резерву перевірок = $245; орієнтовно 2 робочі дні | Потрібні схема, правила оновлення й очищення при зміні справи |
| Підняти поріг до 20 | лише тимчасово | 1 год × $30 + $2 резерву = $32; до половини дня | Вищі витрати контексту; дефект переноситься на довші діалоги |
| Інструкція зберігати числа | ні як єдиний захист | 2 год × $30 + $2 резерву = $62; до половини дня | Залежність від моделі зберігається |

Це планові припущення про ставку, трудовитрати й резерв, а не фактичний рахунок API чи
гарантований строк. Під мандатом Ship it обираємо обмежену схему критичних п’яти полів;
повний дорогий перебір відкладаємо. Новий release gate ще має дати результати до рішення про реліз.

## Останній рядок

**Що обміняли:** 990 звернень повної сітки на 180 обраних та явні залишкові ризики.
**Чого не робимо:** не заявляємо повного покриття, стабільності між днями/мовами та проходження ще не виконаних запусків.
**За яких умов рішення зміниться:** втрата критичного поля на clean, скарга з непокритої комбінації, зміна сумаризатора/схеми справи або підтверджене зростання довгих діалогів.
