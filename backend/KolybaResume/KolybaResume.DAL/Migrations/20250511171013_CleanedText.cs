using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class CleanedText : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "ClearedText",
                table: "Resumes",
                newName: "CleanedText");

            migrationBuilder.AddColumn<string>(
                name: "CleanedText",
                table: "Vacancies",
                type: "text",
                nullable: false,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CleanedText",
                table: "Vacancies");

            migrationBuilder.RenameColumn(
                name: "CleanedText",
                table: "Resumes",
                newName: "ClearedText");
        }
    }
}
