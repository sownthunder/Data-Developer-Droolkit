using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Outlook = Microsoft.Office.Interop.Outlook;
using Microsoft.Office.Tools;
using Microsoft.Office.Tools.Ribbon;

namespace OutlookMailItemTaskPane
{
    public partial class ManageTaskPaneRibbon
    {
        private void ManageTaskPaneRibbon_Load(object sender, RibbonUIEventArgs e)
        {

        }

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

        private void button1_Click(object sender, RibbonControlEventArgs e)
        {
            Outlook.Inspector inspector = (Outlook.Inspector)e.Control.Context;
            InspectorWrapper inspectorWrapper = Globals.ThisAddIn.InspectorWrappers[inspector];
            CustomTaskPane taskPane = inspectorWrapper.CustomTaskPane;

            if (taskPane != null)
            {

                taskPane.Visible = ((RibbonButton)sender).Enabled;

            }
        }
    }
}
