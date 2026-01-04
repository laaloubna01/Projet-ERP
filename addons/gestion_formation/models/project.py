from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class GestionFormation(models.Model):
    _name = "gestion.formation"
    _description = "Gestion des Formations Universitaires"
    _rec_name = "titre"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date_debut desc"

    # Informations de base
    titre = fields.Char(
        string="Titre de la formation", 
        required=True, 
        tracking=True
    )
    
    reference = fields.Char(
        string="Référence", 
        required=True, 
        copy=False, 
        readonly=True, 
        default='New'
    )
    
    type_formation = fields.Selection(
        [
            ("interne", "Formation Interne"),
            ("externe", "Formation Externe")
        ],
        string="Type de formation",
        default="interne",
        required=True,
        tracking=True
    )
    
    categorie_formation = fields.Selection(
        [
            ("continue", "Formation Continue"),
            ("initiale", "Formation Initiale"),
            ("certifiante", "Formation Certifiante"),
            ("qualifiante", "Formation Qualifiante")
        ],
        string="Catégorie",
        required=True,
        tracking=True
    )
    
    # Responsabilité
    responsable_id = fields.Many2one(
        'res.users', 
        string="Responsable de formation",
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )
    
    formateur_ids = fields.Many2many(
        'res.partner',
        'formation_formateur_rel',
        'formation_id',
        'formateur_id',
        string="Formateurs"
    )
    
    # Dates et durée
    date_debut = fields.Date(
        string="Date de début", 
        required=True,
        tracking=True
    )
    
    date_fin = fields.Date(
        string="Date de fin",
        tracking=True
    )
    
    duree_heures = fields.Float(
        string="Durée (heures)",
        compute="_compute_duree",
        store=True
    )
    
    # Statut
    statut = fields.Selection(
        [
            ("brouillon", "Brouillon"),
            ("planifie", "Planifié"),
            ("en_cours", "En cours"),
            ("termine", "Terminé"),
            ("annule", "Annulé")
        ],
        string="Statut",
        default="brouillon",
        tracking=True
    )
    
    # Informations détaillées
    description = fields.Html(string="Description")
    
    objectifs = fields.Text(string="Objectifs pédagogiques")
    
    prerequis = fields.Text(string="Prérequis")
    
    lieu = fields.Char(string="Lieu de formation")
    
    # Participants
    inscrits_ids = fields.Many2many(
        'res.partner',
        'formation_inscrit_rel',
        'formation_id',
        'inscrit_id',
        string="Inscrits"
    )
    
    nombre_inscrits = fields.Integer(
        string="Nombre d'inscrits",
        compute="_compute_nombre_inscrits",
        store=True
    )
    
    capacite_max = fields.Integer(
        string="Capacité maximale",
        default=30
    )
    
    # Documents
    document_ids = fields.One2many(
        'gestion.formation.document',
        'formation_id',
        string="Documents"
    )
    
    # Évaluation
    evaluation = fields.Text(string="Évaluation / Remarques")
    
    note_moyenne = fields.Float(
        string="Note moyenne",
        digits=(3, 2)
    )
    
    # Champs calculés
    active = fields.Boolean(default=True)
    
    color = fields.Integer(string="Couleur", default=0)
    
    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('gestion.formation') or 'New'
        return super(GestionFormation, self).create(vals)
    
    @api.depends('inscrits_ids')
    def _compute_nombre_inscrits(self):
        for record in self:
            record.nombre_inscrits = len(record.inscrits_ids)
    
    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_heures = delta.days * 8  # 8h par jour
            else:
                record.duree_heures = 0
    
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        for record in self:
            if record.date_fin and record.date_debut:
                if record.date_fin < record.date_debut:
                    raise ValidationError("La date de fin doit être postérieure à la date de début!")
    
    @api.constrains('nombre_inscrits', 'capacite_max')
    def _check_capacite(self):
        for record in self:
            if record.nombre_inscrits > record.capacite_max:
                raise ValidationError(f"Capacité maximale dépassée! Maximum: {record.capacite_max}")
    
    # Actions de changement de statut
    def action_planifier(self):
        self.write({'statut': 'planifie'})
    
    def action_demarrer(self):
        self.write({'statut': 'en_cours'})
    
    def action_terminer(self):
        self.write({'statut': 'termine'})
    
    def action_annuler(self):
        self.write({'statut': 'annule'})
    
    # Tâche planifiée pour mise à jour automatique
    @api.model
    def _update_statut_automatique(self):
        today = date.today()
        formations = self.search([('statut', 'in', ['planifie', 'en_cours'])])
        
        for formation in formations:
            if formation.date_fin and formation.date_fin < today:
                formation.statut = 'termine'
            elif formation.date_debut and formation.date_debut <= today and formation.statut == 'planifie':
                formation.statut = 'en_cours'


class GestionFormationDocument(models.Model):
    _name = "gestion.formation.document"
    _description = "Documents de formation"
    _rec_name = "nom"

    formation_id = fields.Many2one(
        'gestion.formation',
        string="Formation",
        required=True,
        ondelete='cascade'
    )
    
    nom = fields.Char(string="Nom du document", required=True)
    
    type_document = fields.Selection(
        [
            ('support', 'Support de cours'),
            ('exercice', 'Exercice'),
            ('evaluation', 'Évaluation'),
            ('autre', 'Autre')
        ],
        string="Type",
        required=True
    )
    
    fichier = fields.Binary(string="Fichier", required=True)
    
    filename = fields.Char(string="Nom du fichier")
    
    description = fields.Text(string="Description")
    
    date_upload = fields.Datetime(
        string="Date d'ajout",
        default=fields.Datetime.now
    )