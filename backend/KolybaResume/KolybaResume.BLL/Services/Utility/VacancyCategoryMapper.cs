using KolybaResume.Common.Enums;

namespace KolybaResume.BLL.Services.Utility;

public static class VacancyCategoryMapper
{
    private static readonly Dictionary<string, JobCategory> Map = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Android"]        = JobCategory.Mobile,
        ["iOS/macOS"]      = JobCategory.Mobile,
        ["Flutter"]        = JobCategory.Mobile,
        ["React Native"]   = JobCategory.Mobile,
        ["Unity"]          = JobCategory.Mobile,

        ["DevOps"]         = JobCategory.Devops,
        ["SysAdmin"]       = JobCategory.Devops,

        ["QA"]             = JobCategory.QA,

        ["Design"]         = JobCategory.UX,
        ["Animator"]       = JobCategory.UX,
        ["Artist"]         = JobCategory.UX,

        ["AI/ML"]          = JobCategory.Data,
        ["Data Engineer"]  = JobCategory.Data,
        ["Data Science"]   = JobCategory.Data,
        ["Big Data"]       = JobCategory.Data,
        ["DBA"]            = JobCategory.Data,

        ["Analyst"]        = JobCategory.BA,

        ["Project Manager"]     = JobCategory.Manager,
        ["Engineering Manager"] = JobCategory.Manager,
        ["Office Manager"]      = JobCategory.Manager,
        ["Account Manager"]     = JobCategory.Manager,
        ["C‑level"]             = JobCategory.Manager,
        ["Scrum Master"]        = JobCategory.Manager,

        ["Marketing"]     = JobCategory.Marketing,
        ["Copywriter"]    = JobCategory.Marketing,
        ["SEO"]           = JobCategory.Marketing,

        ["HR"]            = JobCategory.HR,

        ["Sales"]         = JobCategory.Sales,

        ["Support"]       = JobCategory.CustomerSupport,

        [".NET"]          = JobCategory.Web,
        ["Node.js"]       = JobCategory.Web,
        ["PHP"]           = JobCategory.Web,
        ["Python"]        = JobCategory.Web,
        ["Ruby"]          = JobCategory.Web,
        ["Java"]          = JobCategory.Web,
        ["C++"]           = JobCategory.Web,
        ["Scala"]         = JobCategory.Web,
        ["Golang"]        = JobCategory.Web,
        ["Erlang"]        = JobCategory.Web,
        ["Delphi"]        = JobCategory.Web,
        ["Rust"]          = JobCategory.Web,
        ["Salesforce"]    = JobCategory.Web,
        ["ERP/CRM"]       = JobCategory.Web,
        ["Front End"]     = JobCategory.Web,
        
        ["\"mobile developer\""]   = JobCategory.Mobile,
        ["\"customer support\""]   = JobCategory.CustomerSupport,
        ["\"project manager\""]    = JobCategory.Manager,
        ["devops"]                 = JobCategory.Devops,
        ["\"data analyst\""]       = JobCategory.Data,
        ["qa"]                     = JobCategory.QA,
        ["\"sales manager\""]      = JobCategory.Manager,
        ["\"ux designer\""]        = JobCategory.UX,
    };

    public static JobCategory FromString(string? category)
    {
        return Map.GetValueOrDefault(category?.Trim() ?? "", JobCategory.Other);
    }
}