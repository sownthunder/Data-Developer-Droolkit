using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.Office.Tools.Ribbon;
using Outlook = Microsoft.Office.Interop.Outlook;
using Microsoft.Office.Tools;

namespace TaskLoggerTaskPane
{
    public partial class TaskLoggerTaskPaneRibbon
    {
        private void TaskLoggerTaskPaneRibbon_Load(object sender, RibbonUIEventArgs e)
        {

        }

        // When the user clicks the toggle button, this method hides or displays the custom task pane that is associated with the current INSPECTOR WINDOW
        private void toggleButton1_Click(object sender, RibbonControlEventArgs e)
        {
            Outlook.Inspector inspector = (Outlook.Inspector)e.Control.Context;
            InspectorWrapper inspectorWrapper = Globals.ThisAddIn.InspectorWrappers[inspector];
            CustomTaskPane taskPane = inspectorWrapper.CustomTaskPane;
            if (taskPane != null)
            {
                taskPane.Visible = ((RibbonToggleButton)sender).Checked;
            }
        }
    }
}
