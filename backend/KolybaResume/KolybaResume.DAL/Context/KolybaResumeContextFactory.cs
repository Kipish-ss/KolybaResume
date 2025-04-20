using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using KolybaResume.DAL.Context;

public class KolybaResumeContextFactory : IDesignTimeDbContextFactory<KolybaResumeContext>
{
    public KolybaResumeContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<KolybaResumeContext>();
        var connectionString = "Server=localhost;Database=KolybaResumeDB;Trusted_Connection=True;";

        optionsBuilder.UseSqlServer(connectionString);

        return new KolybaResumeContext(optionsBuilder.Options);
    }
}