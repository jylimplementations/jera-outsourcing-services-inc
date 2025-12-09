/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { WorkEntriesMultiSelectionButtons } from "@hr_work_entry/views/work_entries_buttons";

// Patch the component to remove Replace by buttons
patch(WorkEntriesMultiSelectionButtons.prototype, "removeReplaceButtons", {
    get replaceButtons() {
        return []; // no buttons will be rendered
    },
});
