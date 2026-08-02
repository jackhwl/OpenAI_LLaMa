# Prompt 8: Build the Expense Wrangler

> Instructor note: The Excel must have real formulas. Students open it and edit data, totals recalculate. Show the Dispatch flow: snap photo of receipt from phone.

```
/new

Context: This is build #8 of 10. Brand templates are ready for Excel formatting. You need expense tracking with receipt processing and company-grade Excel reports where ALL totals use real Excel formulas, not hardcoded values.

Instruction: Build an Expense Wrangler automation with the command /expense-wrangler. Two modes, same command:

Immediate mode: User runs /expense-wrangler and pastes a receipt photo, types "$45 lunch at Kinka today", or sends a receipt from Dispatch. Process it immediately: add to Notion, append row to current month's Excel (create if doesn't exist), save receipt to vault, confirm.

Batch mode: User runs /expense-wrangler with no input. Scan Gmail for forwarded receipts since last run, process all files in inbox/ folder (photos, bank CSVs, bank PDFs), cross-reference with bank via Chrome, regenerate the full monthly Excel report. The scheduled monthly cron runs this mode.

Both modes use the same Notion database and the same Excel file. The Excel has 4 sheets with ALL real formulas. Notion for browsing.

Input:
- Gmail MCP (forwarded receipts, order confirmations)
- work/{this}/inbox/ folder for dropped receipt photos, bank CSVs/PDFs
- Python (OCR for receipt images, CSV/PDF parsing for bank statements)
- Chrome (bank login, scrape transactions for cross-reference)
- /xlsx skill, /xlsx-manipulation skill
- brand/config/brand-config.md (branding for Excel)
- Notion MCP (create "Expenses" database under Personal OS parent page)

Output:
- work/08-expense-wrangler/ with categories.md (expense category rules) and vendors.md (learned vendor mappings)
- Command to run the automation
- Notion "Expenses" database with columns: Vendor (title), Date (date), Amount (number dollar), Category (select: Meals/Travel/Software/Office/Subscriptions/Other), Tax Deductible (checkbox), Notes (text), Status (select: Verified/Unmatched/Flagged). Views: "This Month" (filtered), "By Category" (board), "Flagged" (filtered)
- Branded Excel at outputs/reports/ with 4 sheets: Expense Log (raw data), Monthly Summary (=SUMIFS by month/category), Quarterly Summary (=SUMIFS by quarter, QoQ change %), Category Breakdown (totals, % of total, avg per month). ALL formulas, NOT hardcoded values
- vault/projects/expense-wrangler/ with status and receipt data
- Mark "Expense Wrangler" as Done on sprint board
- Schedule: monthly (last day of each month)
"
```

> Open the Excel. Those are real formulas. Your accountant can use this directly.
