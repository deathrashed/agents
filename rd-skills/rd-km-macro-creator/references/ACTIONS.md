# Complete Keyboard Maestro Action Reference

## All 96 Verified Action Types

| Action | Category | Description |
|--------|----------|-------------|
| `ActivateApplication` | Application | Switch to an application |
| `Alert` | UI | Show alert dialog |
| `ApplicationLauncher` | Application | Launch applications |
| `ApplicationsPaletteToggle` | UI | Toggle applications palette |
| `ApplyStyle` | Text | Apply text style |
| `Assert` | Logic | Assert conditions |
| `BringWindowsForward` | Window | Bring windows to front |
| `Cancel` | Control | Cancel macro execution |
| `ClipboardHistorySwitcher` | Clipboard | Clipboard history control |
| `ClipboardSwitcherMacroAction` | Clipboard | Clipboard switcher action |
| `ClipboardSwitcherPaste` | Clipboard | Paste from switcher |
| `Comment` | Meta | Documentation/comment |
| `CustomPrompt` | UI | Custom dialogs |
| `CutCopyPaste` | Clipboard | Copy/paste operations |
| `DeletePastClipboard` | Clipboard | Delete from history |
| `DisplayProgress` | UI | Show progress bar |
| `ExecuteAppleScript` | Script | Run AppleScript |
| `ExecuteJavaScript` | Script | Run JavaScript |
| `ExecuteJavaScriptForAutomation` | Script | JXA automation |
| `ExecuteJavaScriptForCustomPrompt` | Script | JS in custom prompts |
| `ExecuteMacro` | Control | Trigger another macro |
| `ExecuteShellScript` | Script | Run shell commands |
| `ExecuteShortcut` | Application | Run Shortcuts app |
| `ExecuteSubroutine` | Control | Call subroutine |
| `ExecuteSwift` | Script | Run Swift code |
| `File` | File | File operations |
| `Filter` | Text | Text filtering |
| `For` | Loop | For loop iteration |
| `GetFileAttribute` | File | Get file attributes |
| `Group` | Meta | Action grouping |
| `HideAll` | Application | Hide all apps |
| `HideOthers` | Application | Hide other apps |
| `HideSpecificApp` | Application | Hide specific app |
| `IfThenElse` | Logic | Conditional logic |
| `InsertText` | Text | Type text |
| `Log` | Debug | Debug logging |
| `MacroGroupToggle` | UI | Toggle macro group |
| `ManipulateWindow` | Window | Window control |
| `MouseMoveAndClick` | Input | Mouse interaction |
| `NewFolder` | File | Create new folder |
| `Notification` | UI | System notifications |
| `OCRImage` | Image | OCR functionality |
| `Open1File` | File | Open files |
| `OpenURL` | Network | Open URLs |
| `PasteByName` | Clipboard | Paste by filename |
| `Pause` | Control | Pause execution |
| `PauseUntil` | Control | Pause until condition |
| `PlaySound` | Media | Play audio |
| `PlugIn` | Extension | Plugin actions |
| `PressButton` | UI | Press UI buttons |
| `ProgramSwitcher` | Application | App switcher |
| `PromptForFile` | UI | File picker dialog |
| `PromptForRect` | UI | Region selection |
| `PromptForUserInput` | UI | User input dialog |
| `PromptWithList` | UI | List selection dialog |
| `QuickMacro` | Recording | Quick macro recording |
| `QuitAll` | Application | Quit all apps |
| `QuitSpecificApp` | Application | Quit specific app |
| `ReadFile` | File | Read file content |
| `Repeat` | Loop | Repeat loop |
| `ResizeImage` | Image | Image manipulation |
| `Return` | Control | Return from subroutine |
| `SafariControl` | Browser | Safari control |
| `Search` | Text | Text search |
| `SearchRegEx` | Text | Regex search |
| `SearchReplace` | Text | Search and replace |
| `SelectMenuItem` | UI | Menu item selection |
| `Semaphore` | Control | Concurrency control |
| `SetActionDelay` | Control | Set action delay |
| `SetClipboardToImage` | Clipboard | Set clipboard image |
| `SetClipboardToPastClipboard` | Clipboard | Restore previous clipboard |
| `SetClipboardToText` | Clipboard | Set clipboard text |
| `SetDictionaryToJSON` | Data | JSON to dictionary |
| `SetDictionaryValue` | Data | Dictionary operations |
| `SetFileAttribute` | File | Set file attributes |
| `SetFileIcon` | File | Set file icon |
| `SetKeyboardLayout` | Input | Change keyboard layout |
| `SetMacroEnable` | Control | Enable/disable macro |
| `SetNextEngineWindow` | UI | KM window control |
| `SetVariablesToJSON` | Data | Variables to JSON |
| `SetVariableToCalculation` | Data | Math calculations |
| `SetVariableToText` | Data | Variable assignment |
| `ShowAll` | Application | Show all apps |
| `ShowPaletteOfMacros` | UI | Show palette |
| `SimulateKeystroke` | Input | Simulate key presses |
| `SplitPath` | Text | Parse file paths |
| `Substring` | Text | Substring operations |
| `Switch` | Logic | Multi-way condition |
| `SwitchToLastApplication` | Application | Switch to previous app |
| `TransformImage` | Image | Image transformations |
| `TriggerByName` | Control | Trigger macro by name |
| `TryCatch` | Logic | Error handling |
| `Until` | Loop | Until loop |
| `While` | Loop | While loop |
| `WindowSwitcher` | Window | Window switching |
| `WriteFile` | File | Write to files |

## Action Categories

### Scripting
- ExecuteShellScript, ExecuteAppleScript, ExecuteJavaScript, ExecuteJavaScriptForAutomation, ExecuteSwift

### Control Flow
- IfThenElse, Switch, For, While, Repeat, Until, TryCatch, ExecuteSubroutine, Return, Pause, PauseUntil, Cancel, Semaphore

### Variables & Data
- SetVariableToText, SetVariableToCalculation, SetVariablesToJSON, SetDictionaryToJSON, SetDictionaryValue

### Clipboard
- SetClipboardToText, SetClipboardToImage, CutCopyPaste, ClipboardHistorySwitcher, PasteByName

### Text
- InsertText, SearchReplace, SearchRegEx, Search, Filter, SplitPath, Substring

### File
- File, Open1File, WriteFile, ReadFile, NewFolder, GetFileAttribute, SetFileAttribute, SetFileIcon

### Application
- ActivateApplication, QuitSpecificApp, HideSpecificApp, ShowAll, HideAll, SwitchToLastApplication

### Window
- ManipulateWindow, WindowSwitcher, BringWindowsForward

### UI
- PromptForUserInput, PromptForFile, PromptWithList, CustomPrompt, Alert, Notification, PressButton, SelectMenuItem

### Image
- OCRImage, ResizeImage, TransformImage

### Input
- SimulateKeystroke, MouseMoveAndClick, SetKeyboardLayout

### Browser
- SafariControl

## Source

All 96 actions verified from 1,111 macros in:
`/Users/rd/.config/keyboard-maestro/km-backups/2026-04-02_14•12•33/`
