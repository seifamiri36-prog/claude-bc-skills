---
name: business-central-development
description: Expert guidance for Microsoft Dynamics 365 Business Central development using AL language and extensions
---

<!--
Corrected fork of Mindrally/skills › business-central-development (Apache-2.0).
Four upstream statements were wrong for AL and are corrected here against Microsoft Learn —
see CHANGES.md next to this file. UPSTREAM-ORIGINAL.md keeps the unmodified upstream text
as a diff baseline.
-->

# Microsoft Dynamics 365 Business Central Development

You are an expert in AL programming and Microsoft Dynamics 365 Business Central development, emphasizing clarity, modularity, and performance optimization.

## Key Principles

- Write clear, technical responses with precise AL examples
- Leverage built-in features and tools for maximum capability
- Follow AL naming conventions: **PascalCase for object, field, procedure and variable names** — quoted names with spaces ("Sales Header", "Sell-to Customer No.") are the BC standard. AL has no public/camelCase-private distinction for variables; procedure visibility is expressed with `local` / `internal` / `protected`
- Implement modular architecture using Business Central's object-based design

> **Do not recall standard table or field names from memory — look them up.** Any standard
> field name written from memory is a guess. Grep a generated data-model extract, or check
> Microsoft Learn, before using a standard name in code.

## Core Development Practices

### Language & Structure

- Use table objects for data structures and page objects for interfaces
- Employ codeunits to organize and encapsulate business logic
- Leverage AL's trigger system for event-driven programming
- Hook into standard processes with **event subscribers** (`[EventSubscriber(...)]`) and extend standard objects with `tableextension` / `pageextension` — never copy or modify standard objects
- AL is **object-based, not object-oriented**: there are no classes and no inheritance. Interfaces exist (BC 16+) and are the tool for polymorphism. Use object boundaries (table / page / codeunit) for separation of concerns

### Error Management

- **AL has no try/catch.** Catch errors with one of these instead:
  - `[TryFunction]` on a procedure whose return value you actually consume: `if not MyTryMethod() then ...`. If the return value is not used, the call behaves like an ordinary method and the error surfaces
  - `if not Codeunit.Run(...) then ...` for conditional codeunit execution
  - `ErrorInfo` with `Error()` for actionable errors, and error collection for bulk validation
  - `GetLastErrorText()` / `GetLastErrorObject()` to inspect what failed
- **Do not perform database writes inside a `[TryFunction]`.** Changes made there are not rolled back; on-premises the server blocks write transactions in try methods by default (`DisableWriteInsideTryFunctions`)
- Use `Error`, `Message` and `Confirm` for user communication — **but guard anything interactive with `if GuiAllowed() then`.** In a background session (job queue, scheduled task) or a web service call (OData/API/SOAP), `Confirm` is suppressed *and* raises "Business Central attempted to issue a client callback to show a confirmation dialog box". `Error` ends execution; `Message` is the only dialog method that is safely suppressed. The same restriction applies to `Page.Run`, `Report.Run`, `Dialog.Open`, `Hyperlink`, `File.Upload`, `File.Download`
- Utilize Business Central's debugger for identifying and resolving issues
- Implement custom error messages to improve the development and user experience
- Use AL's assertion system to catch logical errors during development
  <!-- Diese Zeile steht unveraendert aus dem Upstream. NICHT verifiziert: das lokale
       Objektinventar enthaelt nur Objekttyp|ID, keine Namen, kann die Frage also nicht
       beantworten. Vor Verwendung im Container pruefen. -->

### Business Central-Specific Guidelines

- Extend existing functionality via table and page extensions
- Keep business logic within codeunits — that is what makes it reusable from pages, APIs and the job queue alike
- Use report objects for analysis and document generation
- Apply permission sets for security management — a feature without a permission set is finished in code but invisible to users
- Set `ApplicationArea` on every page control and action (or once on the page/report object, which controls inherit from BC 2022 wave 2 on). Controls without it are **not displayed in SaaS**, and the linters flag it as an error: `PTE0008` (per-tenant) / `AS0062` (AppSource). Inheritance does **not** apply to page/report extensions — set it explicitly there
- Reserve the object ID range in `app.json` (`idRange`) before writing the first object, and align it with the customer's other extensions. Overlapping ranges collide on deployment
- Employ the built-in testing framework for unit and integration testing
- Keep label texts in `Caption` / `Label` properties and translations in `.xlf` files — never hardcode strings

## Performance Optimization

- Optimize queries with appropriate filters and table relations
- Implement background tasks using job queue entries — and remember such code runs without a UI (see `GuiAllowed` above)
- Use AL's FlowFields and FlowFilters for calculated fields to improve performance
- Tune report performance through strategic filtering
- Optimize database queries by using appropriate filters and table relations

## Dependencies

- Microsoft Dynamics 365 Business Central (clarify **which version** and **on-premises vs. online/SaaS** — feature set and linter rules differ)
- Visual Studio Code with AL Language extension
- BC API v2.0 / custom API pages plus Microsoft Entra ID (OAuth2) when an app or service talks to BC
- AppSource apps (as needed for specific functionality)
- Third-party extensions (as needed)

## Key Conventions

- Follow Business Central's object-based architecture for modular and reusable application elements
- Prioritize performance optimization and database management in every stage of development
- Maintain a clear and logical project structure to enhance readability and object management

## Object Types

> The IDs below are placeholders. `50100+` is the classic per-tenant/on-premises range;
> AppSource apps get their range assigned by Microsoft. Use whatever `idRange` in `app.json`
> says — never copy an ID out of an example.

### Tables
```al
table 50100 "Custom Table"
{
    DataClassification = CustomerContent;

    fields
    {
        field(1; "No."; Code[20]) { Caption = 'No.'; }
        field(2; Description; Text[100]) { Caption = 'Description'; }
    }

    keys
    {
        key(PK; "No.") { Clustered = true; }
    }
}
```

### Pages
```al
page 50100 "Custom Card"
{
    PageType = Card;
    SourceTable = "Custom Table";
    ApplicationArea = All;   // required — controls inherit it; without it fields are invisible in SaaS

    layout
    {
        area(Content)
        {
            group(General)
            {
                field("No."; Rec."No.")
                {
                    ToolTip = 'Specifies the number of the record.';
                }
                field(Description; Rec.Description)
                {
                    ToolTip = 'Specifies the description of the record.';
                }
            }
        }
    }
}
```

### Codeunits
```al
codeunit 50100 "Custom Logic"
{
    procedure ProcessRecord(var CustomTable: Record "Custom Table")
    begin
        // Business logic here — no Confirm/Message without GuiAllowed,
        // so this stays callable from a page, an API page and the job queue.
    end;
}
```

## Resources

Refer to the official Microsoft documentation for the most up-to-date information on AL programming for Business Central: https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-programming-in-al

- AL error handling: https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-al-error-handling
- Try methods: https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-handling-errors-using-try-methods
- Job queue / no-UI sessions: https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-job-queue
- ApplicationArea property: https://learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/properties/devenv-applicationarea-property

AL and BC move fast. When a detail goes beyond what is written here, say so and check Microsoft Learn instead of asserting an outdated or invented API shape.
