using KolybaResume.DAL.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace KolybaResume.DAL.Context.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(50);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(50);

        builder.Property(u => u.ImagePath)
            .HasMaxLength(300);
        
        builder.HasIndex(u => u.Email)
            .IsUnique();
        
        builder.HasIndex(u => u.Uid)
            .IsUnique();
    }
}