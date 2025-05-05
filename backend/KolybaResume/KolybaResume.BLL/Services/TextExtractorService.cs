using System.Text;
using DocumentFormat.OpenXml.Packaging;
using NPOI.HWPF;
using NPOI.HWPF.Extractor;
using UglyToad.PdfPig;
using UglyToad.PdfPig.Content;

namespace KolybaResume.BLL.Services;

public class TextExtractorService
{
    public static string ReadPdf(Stream pdfStream)
    {
        var sb = new StringBuilder();
        using (var document = PdfDocument.Open(pdfStream))
        {
            foreach (Page page in document.GetPages())
            {
                sb.AppendLine(page.Text);
            }
        }
        return sb.ToString();
    }
    
    public static string ReadDocx(Stream docxStream)
    {
        using (var doc = WordprocessingDocument.Open(docxStream, false))
        {
            return doc.MainDocumentPart!.Document.Body!.InnerText;
        }
    }

    public static string ReadDoc(Stream docStream)
    {
        var doc = new HWPFDocument(docStream);
        var extractor = new WordExtractor(doc);
        return extractor.Text;
    }
}