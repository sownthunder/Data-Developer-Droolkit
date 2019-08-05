"""
Created on August 01, 2019

dir to monitor: F:/APPS/CofA/
outbound_path : G:/C of A's/#Email Node/



"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import textwrap, tempfile
import queue, logging
from PyPDF2 import PdfFileReader, PdfFileWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CofACustomHandler(FileSystemEventHandler): #{

    def __init__(self, save_list, out_directory): #{
        self.save_list = save_list
        self.out_directory = out_directory
    #}

    def dispatch(self, event): #{
        # setup variable to hold type
        event_type = str(event.event_type)
        if event_type == "created": #{
            output_str = "CREATED>>>"
            output_str += str("\nis_dir == " + str(event.is_directory) + ">>>")
            output_str += str("\nsrc_path >>> " + str(event.src_path))
            logging.info(textwrap.fill(output_str,
                                       initial_indent='',
                                       subsequent_indent='    ' * 4,
                                       width=65
                                       ))
            # variable to hold PATH of file
            the_event_path = Path(event.src_path)
            # variable to hold file_name ONLY
            the_file_name = os.path.basename(the_event_path)
            # check if file is .PDF
            if fnmatch.fnmatch(the_file_name, "*.pdf"): #{
                # we have a match, SO APPEND TO LIST!
                save_list.append(str(the_event_path))
                # FUNCTION CALL HERE
                move_to_node(the_src_path=the_event_path,
                             the_dst=out_directory
                             )
            #}
            else: #{
                logging.info(">>>NOT A .PDF<<<")
            #}
        #}
        elif event_type == "deleted": #{
            output_str = "DELETED>>>"
            output_str += str("\nis_dir == " + str(event.is_directory) + ">>>")
            output_str += str("\nsrc_path >>> " + str(event.src_path))
            logging.info(textwrap.fill(output_str,
                                       initial_indent='',
                                       subsequent_indent='    ' * 4,
                                       width=65
                                       ))
        #}
        elif event_type == "modified": #{
            output_str = "MODIFIED>>>"
            output_str += str("\nis_dir == " + str(event.is_directory) + ">>>")
            output_str += str("\nsrc_path >>> " + str(event.src_path))
            logging.info(textwrap.fill(output_str,
                                       initial_indent='',
                                       subsequent_indent='    ' * 4,
                                       width=65
                                       ))
        #}
        elif event_type == "moved": #{
            output_str = "MOVED>>>"
            output_str += str("\nis_dir == " + str(event.is_directory) + ">>>")
            output_str += str("\nsrc_path >>> " + str(event.src_path))
            logging.info(textwrap.fill(output_str,
                                       initial_indent='',
                                       subsequent_indent='    ' * 4,
                                       width=65
                                       ))
        #}
    #}
#}

def perform_event_actions_on_file(the_file_path, the_event_type): #{
    print("perform action on event == ")
#}

def create_watermark(input_pdf, output, watermark): # {
    try:  # {
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        pdf_reader = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):  # {
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)
        # }

        with open(output, 'wb') as out:  # {
            pdf_writer.write(out)
        # }
    # }
    except: # {
        errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        logging.error("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        # }
    else: # {
        logging.info("[watermark-pdf] FIN...")
    # }
    return
# }

"""
MOVE NEWLY CREATED .PDFs to 'TEMP' in order to be WATERMARKED
"""
def move_to_node(the_src_path, the_dst): #{
    # GET NEWLY_MADE 'file_name'
    file_name = os.path.basename(the_src_path)
    logging.info("FILE_NAME >>> " + str(file_name))
    # CHECK IF FILE IS OF .PDF
    if fnmatch.fnmatch(file_name, "*.pdf"): #{
        # CREATE TEMP DIR TO WORK INSIDE OF:
        with tempfile.TemporaryDirectory() as directory_name: #{
            the_dir = Path(directory_name)
            logging.info("TEMP_DIRECTORY >>> " + str(the_dir))
            # COPY NEWLY_MADE FILE INTO TEMP_DIR
            shutil.copy(src=Path(the_src_path), dst=the_dir)
            # create temp_file_path from within TEMP_DIR
            temp_path = os.path.join(the_dir, file_name)
            # PERFORM STRING OPERATIONS
            #################################
            idx_mrk = file_name.rfind('@', 0, len(file_name))
            half1 = str(file_name[0:idx_mrk])
            half2 = str(file_name[idx_mrk + 1:len(file_name)])
            logging.info("HALF 1 == " + half1)
            logging.info("HALF 2 == " + half2)
            #  setup NEW FILE NAME (for copy)
            new_name = "part "
            new_name += str(half1)
            new_name += " CofA Lot# "
            new_name += str(half2)
            logging.info("NEW NAME == " + str(new_name))
            #################################
            # CREATE 'new_path' by using "new_name"
            new_path = os.path.join(out_directory, new_name)
            # CREATE WATERMARK AND MOVE FILES OUT OF TEMP_DIR
            create_watermark(input_pdf=temp_path,
                            output=new_path,
                            watermark=in_file)
        #}
        logging.info("Name of temp_dir: " + str(the_dir))
        logging.info("Directory exists after? " + str(the_dir.exists()))
        logging.info("Contents after:" + str(list(the_dir.glob('*'))))
    #}
    else: #{
        logging.info("NOT A .PDF!")
    #}
#}

if __name__ == "__main__":  # {
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            stream=sys.stdout,
                            format='%(asctime)s : %(message)s',  # -%(filename)s-%(funcName)s-%(lineno)s',
                            # '\n\t\t%(asctime)s : %(message)s',  # : %(funcName)s',
                            datefmt='%Y-%m-%d-%H%M%S')
        in_file = "C:/CofA/imp/Agilent_CofA_Letterhead_03-21-19.pdf"
        # in_directory = "F:/APPS/CofA/"
        in_directory = "C:/Temp/F/APPS/CofA/"
        # out_directory = "C:/Temp/"
        out_directory = "C:/Temp/G/C of A's/#Email Node/"
        save_list = []
        observer = Observer()
        event_handler = CofACustomHandler(save_list=save_list,
                                          out_directory=out_directory)
        observer.schedule(event_handler=event_handler,
                          path=in_directory,
                          recursive=True)
        observer.start()
        try:  # {
            while True:  # {
                sleep(1)
            # }
        # }
        except KeyboardInterrupt:  # {
            observer.stop()
        # }
        observer.join()
    # }
    except:  # {
        errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        logging.info("\n" + typeE +
                     "\n" + fileE +
                     "\n" + lineE +
                     "\n" + messageE)
    # }
    else:  # {
        logging.info("[scan-dir] FIN...")
    # }

# }