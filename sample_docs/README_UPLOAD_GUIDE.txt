# Sample Documents — Upload Guide
# Enterprise AI Copilot Demo
# ============================================================
#
# HOW TO USE:
#   1. Start your app (docker-compose up OR npm run dev + uvicorn)
#   2. Register the FIRST account (auto-becomes Admin)
#   3. Register a second account → promote to "employee" from Admin panel
#   4. Register a third account → leave as "user"
#   5. Log in as Admin → go to Documents page → upload each file below
#      with the access level shown in the table.
#   6. Test queries with each role to demo access control!
#
# ============================================================
#
# DOCUMENT UPLOAD TABLE
# ─────────────────────────────────────────────────────────────────────────────────────────
# File                                              | Upload As (Access Level) | Why
# ─────────────────────────────────────────────────────────────────────────────────────────
# TechNova_Q4_2024_Earnings_Report.txt              | all                      | Public earnings report
# TechNova_SEC_Form4_Insider_Trading_Jan2025.txt    | all                      | Public SEC filing
# GreenFin_Banking_10K_Annual_Report_2024.txt       | all                      | Public 10-K report
# TechNova_SEC_8K_MaterialEvent_Feb2025.txt         | all                      | Public 8-K filing
# TechSector_Q1_2025_Market_Outlook.txt             | all                      | Public sector analysis
# AtlasCapital_Client_Investment_Policy_Statement.txt| all                     | Public client doc
# Employee_StockMarket_Fundamentals_Guide.txt       | employee                 | Internal training doc
# AtlasCapital_TNOV_Internal_Research_Note.txt      | employee                 | Confidential research
# AtlasCapital_Portfolio_Risk_Report_Feb2025.txt    | admin                    | Admin-only risk data
# AtlasCapital_InvestmentCommittee_Memo_Mar2025.txt | admin                    | Admin-only IC memo
# ─────────────────────────────────────────────────────────────────────────────────────────
#
# ACCESS LEVEL LOGIC (from your codebase):
#   admin    → visible to Admin only
#   employee → visible to Employee + Admin
#   all      → visible to all roles (User, Employee, Admin)
#
# ============================================================
#
# DEMO SCENARIO: "Who can see what?"
#
#   Role: USER (basic)
#     Can answer questions about:
#       ✅ TechNova Q4 earnings, EPS, revenue, guidance
#       ✅ SEC Form 4 insider trading filings
#       ✅ GreenFin 10-K (capital ratios, legal proceedings)
#       ✅ TechNova 8-K acquisition announcement
#       ✅ Tech sector market outlook
#       ✅ Atlas Capital investment policy / fee structure
#       ❌ Internal equity research (TNOV BUY rating, price target $265)
#       ❌ Portfolio positions, VaR, stress tests
#       ❌ Investment Committee decisions and trading plans
#
#   Role: EMPLOYEE
#     Can answer everything USER can, PLUS:
#       ✅ TNOV internal research note (BUY, target $265, valuation model)
#       ✅ Stock market fundamentals guide (insider trading policy, glossary)
#       ❌ Portfolio risk report (VaR, position sizes, limit breaches)
#       ❌ Investment committee confidential trading decisions
#
#   Role: ADMIN
#     Can answer everything, including:
#       ✅ Portfolio risk report (top 10 positions, stress tests, breaches)
#       ✅ Investment committee memo (TNOV/GFBG decisions, BIOX reduction)
#
# ============================================================
#
# DEMO QUERIES TO TRY (by role)
# ─────────────────────────────────────────────────────────────
#
# As USER (public documents only):
#   1. "What was TechNova's revenue in Q4 2024?"
#      → Q4 revenue $4.82B, +18% YoY
#
#   2. "Did any TechNova insiders sell shares recently?"
#      → CEO sold via 10b5-1 plan, Director Nakamura bought 2,000 shares
#
#   3. "What is the status of GreenFin's AML investigation?"
#      → Under DOJ/FinCEN review, no charges filed as of 10-K date
#
#   4. "What did TechNova acquire in February 2025?"
#      → SecureLayer AI for $1.85B (65% cash, 35% stock)
#
#   5. "What are Atlas Capital's management fees?"
#      → 0.75% for $10-50M AUM, with 10% performance fee above hurdle
#
# As EMPLOYEE (adds internal research):
#   6. "What is the analyst price target for TNOV?"
#      → BUY rating, 12-month target $265 (upgraded from HOLD)
#
#   7. "What is the DCF valuation for TechNova?"
#      → Intrinsic value $252 base, $295 bull, $185 bear case
#
#   8. "Explain the P/E ratio with an example from our portfolio."
#      → From fundamentals guide: TNOV $220 / $13.47 EPS = 16.3x P/E
#
#   9. "What are the insider trading rules I need to follow?"
#      → Pre-clearance required, 60-day holding, blackout periods, no tipping
#
# As ADMIN (full access):
#  10. "What is our largest equity position and its unrealized gain?"
#      → TNOV at 1.80% AUM ($1.12B), unrealized gain $504M (+58.5%)
#
#  11. "Were there any risk limit breaches in February 2025?"
#      → BIOX healthcare sector reached 15.3% (above 15.0% soft limit)
#         Resolved by reducing BIOX on Jan 30
#
#  12. "What did the Investment Committee decide about the GFBG position?"
#      → Stop-loss at $44.00/share; reduce to 0.50% AUM if triggered
#
#  13. "What is Atlas Capital's worst-case stress test loss?"
#      → CVaR (99%, 10-day): -$2.14B (-3.4% of AUM); within board limit
#
#  14. "What action is proposed for the BIOX position before Q2?"
#      → Reduce from 0.95% to 0.50% AUM before Phase 3 trial readout
#
# ============================================================
#
# FICTIONAL DATA NOTICE:
# All companies, individuals, financial figures, and events in these
# documents are entirely fictional and created for demonstration purposes.
# None of this constitutes real investment advice.
#
# Companies: TechNova Corp (TNOV), GreenFin Banking (GFBG), Atlas Capital,
#            SecureLayer AI, BioSynth Pharma, EnergyX Corp — ALL FICTIONAL
#
# ============================================================
