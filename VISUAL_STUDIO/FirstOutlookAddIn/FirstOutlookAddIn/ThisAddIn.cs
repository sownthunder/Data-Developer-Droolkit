using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Outlook = Microsoft.Office.Interop.Outlook;
using Office = Microsoft.Office.Core;

namespace FirstOutlookAddIn
{
    public partial class ThisAddIn
    {

        Outlook.Inspectors inspectors;

        void Inspectors_NewInspector(Microsoft.Office.Interop.Outlook.Inspector Inspector)
        {
            Outlook.MailItem mailItem = Inspector.CurrentItem as Outlook.MailItem;
            if (mailItem != null)
            {
                if (mailItem.EntryID == null)
                {
                    mailItem.Subject = "This text was added by using code";
                    mailItem.Body = "This text was added by using code";
                    mailItem.Display(true);
                }

            }
        }

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {

            CreateMailItem();
            
            inspectors = this.Application.Inspectors;
            inspectors.NewInspector += new Microsoft.Office.Interop.Outlook.InspectorsEvents_NewInspectorEventHandler(Inspectors_NewInspector);

        }

        private void CreateMailItem()
        {
            Outlook.MailItem mailItem = (Outlook.MailItem)
                this.Application.CreateItem(Outlook.OlItemType.olMailItem);
            mailItem.Subject = "This is the subject";
            mailItem.To = "someone@example.com";
            mailItem.Body = "This is a message.";
            mailItem.Importance = Outlook.OlImportance.olImportanceLow;
            mailItem.Display(false);
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            // Note: Outlook no longer raises this event. If you have code that 
            //    must run when Outlook shuts down, see https://go.microsoft.com/fwlink/?LinkId=506785
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
}
