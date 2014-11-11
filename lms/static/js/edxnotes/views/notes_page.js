;(function (define, undefined) {
    'use strict';
    define([
        'jquery', 'underscore', 'backbone', 'js/edxnotes/collections/notes',
        'js/edxnotes/views/note_item'
    ], function ($, _, Backbone, NotesCollection, NoteItemView) {
        var NotesPageView = Backbone.View.extend({
            className: 'edxnotes-page-wrapper',
            initialize: function (options) {
                this.options = options;
            },

            render: function () {
                if (this.collection.length) {
                    this.collection.forEach(function(model) {
                        var item = new NoteItemView({
                            model: model,
                            debug: this.options.debug
                        });
                        item.render().$el.appendTo(this.$el);
                    }, this);
                } else {
                    this.showNoContentMessage();
                }
                this.hideLoadingIndicator();
                return this;
            },

            showNoContentMessage: function () {
                $('.no-content').removeClass('is-hidden');
            },

            hideNoContentMessage: function () {
                $('.no-content').addClass('is-hidden');
            },
            /**
             * Show the page's loading indicator.
             */
            showLoadingIndicator: function() {
                $('.ui-loading').removeClass('is-hidden');
            },

            /**
             * Hide the page's loading indicator.
             */
            hideLoadingIndicator: function() {
                $('.ui-loading').addClass('is-hidden');
            }
        });

        return function (notesList, debugMode) {
            var collection = new NotesCollection(notesList, {parse: true}),
                view = new NotesPageView({
                    collection: collection,
                    debug: debugMode
                }).render();
            $('.content-primary').append(view.$el);
        };
    });
}).call(this, define || RequireJS.define);
