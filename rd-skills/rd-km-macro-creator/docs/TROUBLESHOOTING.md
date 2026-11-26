# The Complete Story: How We Finally Made Working KM Macros

## The Starting Point

You shared this forum post: https://forum.keyboardmaestro.com/t/chatgpt-built-a-working-exportable-macro-that-imported-to-keyboard-maestro-without-errors/49936

This post revealed a critical insight: ChatGPT CAN generate valid KM macros IF you show it real exports first.

## My Initial Approach

I tried generating kmacros WITHOUT looking at your real backups first:

### First Attempt (WRONG):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Name</key><string>Taio: Text Case</string>
    <key>Actions</key><array>
        <dict>
            <key>Action</key><string>Execute Shell Script</string>
            <key>Parameters</key><dict>
                <key>Script</key><string>tr '[:lower:]' '[:upper:]'</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
```

### Problems With This Approach:

1. **Root was `<dict>` instead of `<array>`** - KM expects `<array>` at root
2. **Used `key>Action`** - Should be `key>MacroActionType`
3. **No `ActionUID`** - Every action needs unique integer ID
4. **No macro-level `UID`** - Each macro needs UID
5. **No trigger dictionary** - Macros need triggers defined
6. **No group-level structure** - Missing "Global Macro Group" wrapping
7. **No `Activate` key** - Required at group level
8. **Wrong hierarchy** - Missing Macros array wrapping

## What I Found In Your Real Macros

After analyzing `/Users/rd/.config/keyboard-maestro/km-backups/2026-04-02_14•10•10/Global Macro Group/Calculate.kmmacros`:

### REAL Structure (Working):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<array>
    <dict>
        <key>Activate</key><string>Normal</string>
        <key>Macros</key><array>
            <dict>
                <key>Actions</key><array>
                    <dict>
                        <key>ActionUID</key><integer>100317937</integer>
                        <key>MacroActionType</key><string>PromptForUserInput</string>
                        <key>Title</key><string>Calculate</string>
                        <key>Variables</key><array>
                            <dict>
                                <key>Default</key><string>%Variable%Calculation%</string>
                                <key>Variable</key><string>Calculation</string>
                            </dict>
                        </array>
                    </dict>
                    <!-- more actions -->
                </array>
                <key>Name</key><string>Calculate</string>
                <key>Triggers</key><array>
                    <dict><key>MacroTriggerType</key><string>StatusMenu</string></dict>
                </array>
                <key>UID</key><string>71B5B59F-37D9-4944-86DD-9386F66D6281</string>
            </dict>
        </array>
        <key>Name</key><string>Global Macro Group</string>
        <key>UID</key><string>804D32AF-0B39-439F-8EF3-493A833B14CA</string>
    </dict>
</array>
</plist>
```

### Key Differences Found:

| Wrong | Correct |
|-------|---------|
| `<dict>` root | `<array>` root |
| `Action` | `MacroActionType` |
| No `ActionUID` | Each action has unique integer |
| No group-level keys | Has `Activate`, `Macros`, `Name`, `UID` |
| No triggers array | Has `Triggers` → `MacroTriggerType` |
| Wrong variable syntax | `%Variable%Name%` |
| Missing `CreationDate` | Optional but present in real |
| Missing nested structure | Actions inside `Macros` → `dict` |

## Complex Macros Found

Looking at your backups in `2026-04-02_14•12•33/`:

### Simple Macros (Working):
- `Global Macro Group/Calculate.kmmacros` - Basic input/calculate/output
- `Global Macro Group/Empty Trash.kmmacros` - Single action

### Complex Macros (Examples):
1. **`•main | MAIN MACRO`** - 404 lines, complex folder structure
2. **`dbase | 10 Run database action.kmmacros`** - Database operations
3. **`subs | 80 The MultiTimer.kmmacros`** - Timer system
4. **`tasks | 00 Create a new backup.kmmacros`** - Backup creation

### Patterns Found in Complex Macros:

1. **Conditional Logic**: `IfThenElse` with `Conditions`, `ThenActions`, `ElseActions`
2. **Looping**: Multiple actions chained
3. **Variable Manipulation**: Set/Get/Modify variables
4. **Sub-macros**: Calling other macros
5. **Error Handling**: Try/catch style with conditionals
6. **Timing**: Delays, waits

### Common Complex Actions Found:

```xml
<!-- If Then Else -->
<dict>
    <key>MacroActionType</key><string>IfThenElse</string>
    <key>Conditions</key><dict>
        <key>ConditionList</key><array>
            <dict>
                <key>ConditionType</key><string>Variable</string>
                <key>Variable</key><string>Result Button</string>
                <key>VariableConditionType</key><string>Contains</string>
                <key>VariableValue</key><string>Copy</string>
            </dict>
        </array>
    </dict>
    <key>ThenActions</key><array>...</array>
    <key>ElseActions</key><array>...</array>
</dict>

<!-- Execute Shell Script -->
<dict>
    <key>MacroActionType</key><string>ExecuteShellScript</string>
    <key>Parameters</key><dict>
        <key>Script</key><string>echo hello</string>
        <key>Shell</key><string>/bin/bash</string>
    </dict>
</dict>
```

## The Fix Process

### Step 1: Study Real Export
```bash
# Find backup location
ls /Users/rd/.config/keyboard-maestro/km-backups/

# Look at simple macro structure  
cat "Global Macro Group/Calculate.kmmacros" | head -100
```

### Step 2: Copy The Blueprint
- Root is `<array>`
- Each macro group wrapped in `<dict>`
- Macros go in `<Macros><array><dict>`
- Actions go in `<Actions><array><dict>`

### Step 2.5: Separate Wrapper from Action Schema

This turned out to be the most useful mental model:

- The plist wrapper is fairly stable and can be templated.
- The action body is where imports usually break.

In practice that means:

- hand-write the wrapper only if it matches known-good exports
- clone `ExecuteShellScript`, `PromptForUserInput`, `ActivateApplication`, `SimulateKeystroke`, and other non-trivial actions from real exports
- only edit payload fields unless another export proves a structural variation is valid

### Step 3: Always Validate
```bash
plutil -lint your-macro.kmmacros
```

Important: this only verifies plist syntax. A file can pass `plutil` and still crash or fail on KM import if the action schema is wrong.

### Step 4: Fix Common Errors

| Error | Fix |
|-------|-----|
| "Invalid structure" | Check root is `<array>` |
| "Unknown action" | Export real macro to get exact name |
| "Import failed" | Validate first |
| "Variable not found" | Use `%Variable%Name%` |

## Reference Actions Found

From your complex macros, here are action names that work:

- `PromptForUserInput`
- `SetVariableToText`
- `SetClipboardToText`
- `GetClipboard`
- `ExecuteShellScript`
- `IfThenElse`
- `Filter` (for calculations)
- `Display`
- `Alert`
- `OpenURL`

## What Made It Work

The key insight from that forum post:
> **Provide example exports to the LLM first, then it can replicate the exact schema**

Without seeing your real exports, I couldn't know:
1. The root is array not dict
2. Action UID must be integer
3. MacroActionType not Action
4. Trigger structure required

Now we have the complete solution documented.
