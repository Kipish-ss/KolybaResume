using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddResumeKeywords : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Keywords",
                table: "Resumes",
                type: "text",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Keywords",
                table: "Resumes");
        }
    }
}
