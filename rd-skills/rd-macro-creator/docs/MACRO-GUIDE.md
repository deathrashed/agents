# Keyboard Maestro Macro Creation Guide

## Why This Is Hard

LLMs (ChatGPT, Claude, etc.) generate "what a response would look like" — not what the response SHOULD be. They hallucinate Keyboard Maestro's internal XML schema because:

1. **KM uses a complex, undocumented plist structure**
2. **No public schema is available for LLMs to learn from**
3. **Small typos in keys cause complete import failure**

## The Solution

**Study real exports** from your own Keyboard Maestro library. This is what the forum post proved works.

## The Most Important Distinction

There are two very different things in a `.kmmacros` file:

1. The outer plist/group/macro wrapper, which is relatively stable
2. The individual action dictionaries, which are often schema-sensitive and easy to get subtly wrong

Use the wrapper as a guide. Use real exports as the source of truth for action bodies.

---

## Anatomy of a .kmmacros File

### 1. Root Structure (Always Array)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
    <dict>
        <!-- Macro Group Starts Here -->
    </dict>
</array>
</plist>
```

### 2. Required Group-Level Keys

| Key | Type | Description |
|-----|------|-------------|
| `Activate` | string | "Normal" (almost always) |
| `Macros` | array | Array of macro dicts |
| `Name` | string | Display name in KM |
| `UID` | string | Unique identifier (format: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX) |

### 3. Required Macro-Level Keys

| Key | Type | Description |
|-----|------|-------------|
| `Actions` | array | Array of action dicts |
| `Name` | string | Macro name (user-facing) |
| `Triggers` | array | What triggers the macro |
| `UID` | string | Unique macro ID |

### 4. Action Structure

Each action needs:
- `ActionUID` - Integer (unique within macro)
- `MacroActionType` - The KM action name (e.g., "ExecuteShellScript", "SetVariableToText")

```xml
<dict>
    <key>ActionUID</key><integer>1001</integer>
    <key>MacroActionType</key><string>ActionNameFromRealExport</string>
    <!-- Remaining keys should match a real exported action block -->
</dict>
```

---

## Safe and Unsafe Examples

### Safe to use as a hand-written guide

- Root plist structure
- Group-level keys
- Macro-level keys
- Simple status menu trigger shape

### Unsafe to use as authoritative by themselves

- Simplified `ExecuteShellScript` bodies
- Simplified `PromptForUserInput` bodies
- Simplified `ActivateApplication` bodies
- Simplified `SimulateKeystroke` bodies

For those, copy from a real export instead of relying on a guide snippet.

## Common Actions Reference

### Execute Shell Script

```xml
<dict>
    <!-- Do not invent this structure from the guide alone. -->
    <!-- Clone an ExecuteShellScript action from a real export and edit only the payload fields. -->
</dict>
```

### Set Variable to Text

```xml
<dict>
    <key>ActionUID</key><integer>1002</integer>
    <key>MacroActionType</key><string>SetVariableToText</string>
    <key>Text</key><string>%Clipboard%</string>
    <key>Variable</key><string>MyVariable</string>
</dict>
```

### Set Clipboard to Text

```xml
<dict>
    <key>ActionUID</key><integer>1003</integer>
    <key>MacroActionType</key><string>SetClipboardToText</string>
    <key>Text</key><string>%Variable%Result%</string>
</dict>
```

### If Then Else

```xml
<dict>
    <key>ActionUID</key><integer>1004</integer>
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
    <key>ThenActions</key><array>
        <dict>
            <key>MacroActionType</key><string>SetClipboardToText</string>
            <key>Text</key><string>%Variable%Result%</string>
        </dict>
    </array>
    <key>ElseActions</key><array>
        <!-- else actions here -->
    </array>
</dict>
```

### Prompt for User Input

```xml
<dict>
    <!-- Clone from a real export. Prompt actions vary more than they look. -->
</dict>
```

---

## Variables Reference

| Variable | Meaning |
|----------|---------|
| `%Clipboard%` | Current clipboard content |
| `%Variable%Name%` | Variable named "Name" |
| `%System%Date%` | Current date |
| `%System%Time%` | Current time |

---

## Complete Working Example

This macro reads clipboard, uppercases it, and writes back:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
    <dict>
        <key>Activate</key><string>Normal</string>
        <key>Macros</key><array>
            <dict>
                <key>Actions</key><array>
                    <dict>
                        <key>ActionUID</key><integer>1001</integer>
                        <key>MacroActionType</key><string>SetVariableToText</string>
                        <key>Text</key><string>%Clipboard%</string>
                        <key>Variable</key><string>InputText</string>
                    </dict>
                    <!-- For a real macro, clone the shell-script action from a real export -->
                    <dict>
                        <key>ActionUID</key><integer>1003</integer>
                        <key>MacroActionType</key><string>SetClipboardToText</string>
                        <key>Text</key><string>%Variable%Result%</string>
                    </dict>
                </array>
                <key>Name</key><string>Uppercase Clipboard</string>
                <key>Triggers</key><array>
                    <dict><key>MacroTriggerType</key><string>StatusMenu</string></dict>
                </array>
                <key>UID</key><string>MY-UPPER-001</string>
            </dict>
        </array>
        <key>Name</key><string>Global Macro Group</string>
        <key>UID</key><string>MY-GROUP-001</string>
    </dict>
</array>
</plist>
```

---

## How to Find More Actions

1. **Export a simple KM macro** with the action you need
2. **Open the .kmmacros file** in a text editor
3. **Copy the action block** into your new macro
4. **Modify payload fields only** unless you have confirmed the rest of the structure from another export

---

## Validation Commands

```bash
# Validate plist syntax
plutil -lint Macro.kmmacros

# Convert to XML for viewing
plutil -convert xml1 Macro.kmmacros -o - | less
```

Remember: passing `plutil -lint` means "well-formed plist", not "safe to import in Keyboard Maestro".

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `<dict>` at root | Use `<array>` at root |
| Missing `MacroActionType` | Every action needs this key |
| Wrong action name | Export real macro to get exact name |
| Missing `ActionUID` | Give each action a unique integer |
| Forgetting `<key>` tags | Every key needs `<key>` tag |
| Wrong variable syntax | Use `%Variable%Name%` format |

---

## Quick Reference Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
    <dict>
        <key>Activate</key><string>Normal</string>
        <key>Macros</key><array>
            <dict>
                <key>Actions</key><array>
                    <!-- ACTIONS HERE -->
                </array>
                <key>Name</key><string>MACRO NAME</string>
                <key>Triggers</key><array>
                    <dict><key>MacroTriggerType</key><string>StatusMenu</string></dict>
                </array>
                <key>UID</key><string>UID-HERE</string>
            </dict>
        </array>
        <key>Name</key><string>Global Macro Group</string>
        <key>UID</key><string>GROUP-UID</string>
    </dict>
</array>
</plist>
```

---

## Sources

- Original forum post: https://forum.keyboardmaestro.com/t/chatgpt-built-a-working-exportable-macro-that-imported-to-keyboard-maestro-without-errors/49936
- Example exports from: `/Users/rd/.config/keyboard-maestro/km-backups/`
