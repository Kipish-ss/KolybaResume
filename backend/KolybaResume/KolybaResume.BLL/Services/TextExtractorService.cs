using System.Text;
using DocumentFormat.OpenXml.Packaging;
using NPOI.HWPF;
using NPOI.HWPF.Extractor;
using UglyToad.PdfPig;

namespace KolybaResume.BLL.Services;

public static class TextExtractorService
{
    public static string ReadPdf(Stream stream)
    {
        var sb = new StringBuilder();
        using (var document = PdfDocument.Open(stream))
        {
            foreach (var page in document.GetPages())
            {
                sb.AppendLine(page.Text);
            }
        }
        return sb.ToString();
    }
    
    public static string ReadDocx(Stream stream)
    {
        using var document = WordprocessingDocument.Open(stream, false);
        return document.MainDocumentPart!.Document.Body!.InnerText;
    }

    public static string ReadDoc(Stream stream)
    {
        var document = new HWPFDocument(stream);
        var extractor = new WordExtractor(document);
        return extractor.Text;
    }
}