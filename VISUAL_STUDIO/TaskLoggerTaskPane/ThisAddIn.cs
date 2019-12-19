using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Outlook = Microsoft.Office.Interop.Outlook;
using Office = Microsoft.Office.Core;
using Microsoft.Office.Tools;

namespace TaskLoggerTaskPane
{
    public partial class ThisAddIn
    {

        private Dictionary<Outlook.Inspector, InspectorWrapper> inspectorWrappersValue =
            new Dictionary<Outlook.Inspector, InspectorWrapper>();
        private Outlook.Inspectors inspectors;

        // [2019-12-19]
        private TaskPaneControl myTaskPaneControl1;
        private Microsoft.Office.Tools.CustomTaskPane myCustomTaskPane;

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            // [2019-12-19]
            myTaskPaneControl1 = new TaskPaneControl();
            myCustomTaskPane = this.CustomTaskPanes.Add(myTaskPaneControl1, "IT Task Logger");
            myCustomTaskPane.Visible = true;

            // [2019-12-19]
            // REMOV ETHIS FOR [NEW MAIL ITEM] FUNCTIONALITY
            inspectors = this.Application.Inspectors;
            inspectors.NewInspector +=
                new Outlook.InspectorsEvents_NewInspectorEventHandler(
                    Inspectors_NewInspector);

            foreach (Outlook.Inspector inspector in inspectors)
            {
                Inspectors_NewInspector(inspector);
            }

        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            // Note: Outlook no longer raises this event. If you have code that 
            //    must run when Outlook shuts down, see https://go.microsoft.com/fwlink/?LinkId=506785

            // [2019-12-19] 
            // REMOVE THIS FOR [NEW MAIL ITEM] FUNCTIONALITY
            inspectors.NewInspector -=
                new Outlook.InspectorsEvents_NewInspectorEventHandler(
                    Inspectors_NewInspector);
            inspectors = null;
            inspectorWrappersValue = null;

        }

        void Inspectors_NewInspector(Outlook.Inspector Inspector)
        {

            // IF A NEW INSPECTOR CONTAINS AN EMAIL MESSAGE, AN INSTANCE IS CREATED
            // of "InspectorWrapper" to manage the relationship between email message and task pane
            if (Inspector.CurrentItem is Outlook.MailItem)
            {
                inspectorWrappersValue.Add(Inspector, new InspectorWrapper(Inspector));
            }
        }

        // This property exposes the private "inspectorWrappersValue" field to code OUTSIDE the "ThisAddIn" class.
        public Dictionary<Outlook.Inspector, InspectorWrapper> InspectorWrappers
        {
            get
            {
                return inspectorWrappersValue;
            }
        }

        #region VSTO generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InternalStartup()
        {
            this.Startup += new System.EventHandler(ThisAddIn_Startup);
            this.Shutdown += new System.EventHandler(ThisAddIn_Shutdown);
        }
        
        #endregion
    }

    public class InspectorWrapper
    {

        private Outlook.Inspector inspector;
        private CustomTaskPane taskPane;

        public InspectorWrapper(Outlook.Inspector Inspector)
        {

            inspector = Inspector;
            ((Outlook.InspectorEvents_Event)inspector).Close +=
                new Outlook.InspectorEvents_CloseEventHandler(InspectorWrapper_Close);

            taskPane = Globals.ThisAddIn.CustomTaskPanes.Add(
                new TaskPaneControl(), "My IT Tasks", inspector);
            taskPane.VisibleChanged += new EventHandler(TaskPane_VisibleChanged);

        }

        void TaskPane_VisibleChanged(object sender, EventArgs e)
        {

            Globals.Ribbons[inspector].TaskLoggerTaskPaneRibboncs.toggleButton1.Checked =
                taskPane.Visible;

        }

        void InspectorWrapper_Close()
        {

            if (taskPane != null)
            {
                Globals.ThisAddIn.CustomTaskPanes.Remove(taskPane);
            }

            taskPane = null;
            Globals.ThisAddIn.InspectorWrappers.Remove(inspector);
            ((Outlook.InspectorEvents_Event)inspector).Close -=
                new Outlook.InspectorEvents_CloseEventHandler(InspectorWrapper_Close);
            inspector = null;

        }

        public CustomTaskPane CustomTaskPane
        {

            get
            {

                return taskPane;

            }
        }
    }
}
